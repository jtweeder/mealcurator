from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from meals.models import mstr_recipe
from stewpot.models import share_meal, meal_posting
from mealcurator.helperfuncs import check_blank, AICreateMeal


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

@login_required
@user_passes_test(staff_check)
def recipe_ai_create(request):
    
    if request.method == 'POST':
        ing1 = request.POST.get('ing-1')
        ing2 = request.POST.get('ing-2')
        ing3 = request.POST.get('ing-3')
        ing4 = request.POST.get('ing-4')
        ing5 = request.POST.get('ing-5')
        mode = request.POST.get('mode')
        time = request.POST.get('time')
        other = request.POST.get('other')

        ingredients = []
        for ing in [ing1, ing2, ing3, ing4, ing5]:
            if len(ing) > 0:
                ingredients.append(ing)
        
        ai_resp = AICreateMeal(ingredients, mode, time, other)
    # TODO: Create DB object to story request for AI if users wants to save
    # TODO: Create a page to hold the recipe with information about how it was generated
       