from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.defaultfilters import slugify
from django.utils.html import format_html
from meals.models import mstr_recipe, raw_recipe
from stewpot.models import share_meal, meal_posting, ai_html
from mealcurator.helperfuncs import check_blank, AICreateMeal
import time


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


@login_required
@user_passes_test(staff_check)
def recipe_ai_create(request):
    
    if request.method == 'POST':
        if request.POST.get('discard') == 'Discard':
            return redirect('ai-recipe-start')
        
        if request.POST.get('submit') == 'Submit':
            ing1 = request.POST.get('ing-1')
            ing2 = request.POST.get('ing-2')
            ing3 = request.POST.get('ing-3')
            ing4 = request.POST.get('ing-4')
            ing5 = request.POST.get('ing-5')
            mode = request.POST.get('mode')
            cook_time = request.POST.get('time')
            other = request.POST.get('other')

            ingredients = []
            for ing in [ing1, ing2, ing3, ing4, ing5]:
                if len(ing) > 0:
                    ingredients.append(ing)
        
            ai_resp = AICreateMeal(ingredients, mode, cook_time, other)
            title, body = ai_resp.clean_response()
            context = {'title': title, 'body': body, 'preview': True}
            template = 'stewpot/ai_recipe.html'
            return render(request, template, context)
        
        elif request.POST.get('save') == 'Save':
            # Create raw_recipe of ai-made recipe and then save the html to ai_html
            title = request.POST.get('title')
            body = request.POST.get('body')
            # TODO: Make the date part of the slug with a -
            slug = slugify(title+'-'+str(int(time.time())))
            # TODO: make this not depend on the site - look at reverse or get script prefix       
            rec_url = 'https://www.mealcurator.com/share/view/ai/'+slug

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
            # TODO: Does not seem to be doing anything -- writes to raw but no mstr - pry fails
            outcome = ai_recipe.pull_mstr()
            if outcome:
                ai_recipe.mstr_flag = True
                ai_recipe_html.meal = mstr_recipe.objects.get(rec_url=rec_url)
                ai_recipe.save()
                ai_recipe_html.save()
                return redirect('view-ai-html', slug)

        
    
def view_ai_recipe(request, ai_html_id):
    ai_recipe = ai_html.objects.get(html_id=ai_html_id)
    context = {'title': ai_recipe.title, 'body': ai_recipe.body, 'view': True}
    template = 'stewpot/ai_recipe.html'
    return render(request, template, context)
    
       