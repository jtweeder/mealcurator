from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.defaultfilters import slugify
from django.utils.html import format_html
from meals.models import mstr_recipe, raw_recipe
from stewpot.models import share_meal, meal_posting, ai_html
from cooks.models import plan
from mealcurator.helperfuncs import check_blank, AICreateMeal, AIRecipeError
import time
import uuid
from openai import APIError, RateLimitError

# TODO:  Let edits happen for things people shared
# TODO:  Let someone add a shared recipe to a list/make a list
# TODO: Let Admins make multiple recipes and make a blogpost about them

def staff_check(user):
    return user.is_staff

@login_required
def start_share(request, meal_id):
    """Landing page for capturing title and text from user"""
    meal = mstr_recipe.objects.get(meal_id=meal_id)
    template = 'stewpot/share.html'
    context = {'meal': meal, 'start': True}
    return render(request, template, context)

@login_required
def save_share(request):
    """Create share_meal and redirect to view of it"""
    if request.method == 'POST':
        shared_title = check_blank(request.POST.get('shared_title'),
                                   'A shared recipe from mealCurator')
        shared_text = check_blank(request.POST.get('shared_text'),
                                  'I found this on mealCurator and wanted to share it with you')
        shared_meal = mstr_recipe.objects.get(meal_id=request.POST.get('shared_meal'))

        shared = share_meal.objects.create(
                    title=shared_title,
                    creator=request.user,
                    text=shared_text,
                    meal=shared_meal,
                    )
    return redirect('view-shared', shared.id)

# View a shared meal
def view_share(request, share_id):
    shared = (share_meal.objects.values('id',
                                        'title',
                                        'text',
                                        'meal_id',
                                        'meal__title',
                                        'meal__vegan',
                                        'meal__vegetarian',
                                        'meal__meal_time',
                                        'meal__cooking_time',
                                        'meal__dish_type',
                                        'meal__cooking_method',
                                        'meal__protein_type',
                                        'meal__rec_url')
                                .filter(id=share_id))
    context = {'shared_meals': shared,
               'view': True
               }
    template = 'stewpot/share.html'
    return render(request, template, context)


def view_posting(request, post_id):
    posting = meal_posting.objects.get(id=post_id)
    shared = (share_meal.objects.values('id',
                                        'title',
                                        'text',
                                        'meal_id',
                                        'meal__title',
                                        'meal__vegan',
                                        'meal__vegetarian',
                                        'meal__meal_time',
                                        'meal__cooking_time',
                                        'meal__dish_type',
                                        'meal__cooking_method',
                                        'meal__protein_type',
                                        'meal__rec_url')
                                .filter(posting=posting))

    context = {'pp': posting,
               'shared_meals': shared}
    template = 'stewpot/meal_post.html'
    return render(request, template, context)

def home_postings(request):
    posts = meal_posting.objects.all().order_by('created_on')
    context = {'posts': posts}
    template = 'stewpot/postings.html'
    return render(request, template, context)


# Check login and provide start of AI Page
@login_required
@user_passes_test(staff_check)
def recipe_ai_start(request):
    template = 'stewpot/ai_recipe.html'
    context = {'start': True}
    return render(request, template, context)

def _build_ai_html_slug(title):
    """Build a unique slug that fits ai_html.html_id max_length."""
    max_len = ai_html._meta.get_field('html_id').max_length or 50
    ts = str(int(time.time()))
    base = slugify(title) or 'ai-recipe'

    # Reserve room for hyphen + timestamp
    reserve = len(ts) + 1
    base_len = max(1, max_len - reserve)
    slug = f'{base[:base_len]}-{ts}'

    # Extremely unlikely collision handling while preserving max length
    while ai_html.objects.filter(html_id=slug).exists():
        rand = uuid.uuid4().hex[:6]
        reserve = len(ts) + len(rand) + 2
        base_len = max(1, max_len - reserve)
        slug = f'{base[:base_len]}-{ts}-{rand}'

    return slug

@login_required
@user_passes_test(staff_check)
def recipe_ai_create(request):
    
    if request.method == 'POST':
        if request.POST.get('discard') == 'Discard':
            return redirect('ai-recipe-start')
        
        if request.POST.get('submit') == 'Submit':
            ingredients_text = check_blank(request.POST.get('ingredients_text', ''), '').strip()
            request_text = check_blank(request.POST.get('request_text', ''), '').strip()

            # Backward-compatible fallback if older form fields are submitted
            if len(ingredients_text) == 0:
                legacy_ingredients = [
                    request.POST.get('ing-1', '').strip(),
                    request.POST.get('ing-2', '').strip(),
                    request.POST.get('ing-3', '').strip(),
                    request.POST.get('ing-4', '').strip(),
                    request.POST.get('ing-5', '').strip(),
                ]
                ingredients_text = ', '.join([x for x in legacy_ingredients if len(x) > 0])

            if len(request_text) == 0:
                mode = request.POST.get('mode', '').strip()
                cook_time = request.POST.get('time', '').strip()
                other = request.POST.get('other', '').strip()
                request_text = ' '.join([x for x in [mode, cook_time, other] if len(x) > 0])

            try:
                ai_resp = AICreateMeal(ingredients_text, request_text)
                title, body = ai_resp.clean_response()
                context = {'title': title, 'body': body, 'preview': True}
                template = 'stewpot/ai_recipe.html'
                return render(request, template, context)
            except RateLimitError as err:
                err_text = str(err)
                if 'insufficient_quota' in err_text:
                    friendly_error = 'OpenAI quota exceeded for this API key. Please check billing, usage limits, and project key selection in your OpenAI account.'
                else:
                    friendly_error = 'OpenAI rate limit reached. Please wait a moment and try again.'

                context = {
                    'start': True,
                    'error_message': friendly_error,
                    'ingredients_text': ingredients_text,
                    'request_text': request_text,
                }
                return render(request, 'stewpot/ai_recipe.html', context)
            except APIError:
                context = {
                    'start': True,
                    'error_message': 'OpenAI service is temporarily unavailable. Please try again shortly.',
                    'ingredients_text': ingredients_text,
                    'request_text': request_text,
                }
                return render(request, 'stewpot/ai_recipe.html', context)
            except AIRecipeError as err:
                context = {
                    'start': True,
                    'error_message': str(err),
                    'ingredients_text': ingredients_text,
                    'request_text': request_text,
                }
                return render(request, 'stewpot/ai_recipe.html', context)
            except Exception:
                context = {
                    'start': True,
                    'error_message': 'Recipe generation failed unexpectedly. Please verify your OpenAI API key and try again.',
                    'ingredients_text': ingredients_text,
                    'request_text': request_text,
                }
                return render(request, 'stewpot/ai_recipe.html', context)
        
        elif request.POST.get('save') == 'Save':
            # Create raw_recipe of ai-made recipe and then save the html to ai_html
            title = request.POST.get('title')
            body = request.POST.get('body')
            slug = _build_ai_html_slug(title)
            rec_url = request.build_absolute_uri('/share/view/ai/') + slug

            ai_recipe_html = ai_html.objects.create(
                html_id=slug,
                title=title,
                creator=request.user,
                body=body
            )            

            ai_recipe = raw_recipe.objects.create(
                title=title,
                rec_url=rec_url,
                vegan=False,
                vegetarian=False,
                meal_time='na',
                dish_type='na',
                protein_type='na',
                cooking_method='na',
                cooking_time='na',
                ai_recipe=True
            )
           
            outcome = ai_recipe.pull_mstr()
            if outcome:
                ai_recipe.mstr_flag = True
                ai_recipe_html.meal = mstr_recipe.objects.get(rec_url=rec_url)
                ai_recipe.save()
                ai_recipe_html.save()
                request.session['from_save'] = True
                return redirect('view-ai-html', slug)        
    
def view_ai_recipe(request, ai_html_id, from_save=False):
    ai_recipe = ai_html.objects.get(html_id=ai_html_id)   
    if request.session.get('from_save', False):
        # Pull the users cooks.plan that are not soft_deleted
        plans = plan.objects.filter(owner=request.user, soft_delete=False)
        context = {'ai_recipe': ai_recipe, 'plans': plans, 'view': True, 'from_save': True}   
        request.session['from_save'] = False
    else:
        context = {'ai_recipe': ai_recipe, 'view': True, 'from_save': False}   
    template = 'stewpot/ai_recipe.html'
    return render(request, template, context)
    
       