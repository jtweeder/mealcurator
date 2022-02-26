from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.db.models import F
from django.views.generic.edit import CreateView
from cooks.models import plan, plan_meal
from meals.models import mstr_recipe, meal_time_choices, dish_type_choices, cooking_method_choices, cook_time_choices
from .forms import create_cook_form


def register_cook(request):
    form = create_cook_form
    if request.method == 'POST':
        form = create_cook_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form': form}
    return render(request, 'registration/register.html', context=context)


@login_required
def cook_profile(request):
    user = request.user
    name = f'{user.first_name} {user.last_name}'
    email = user.email
    # TODO: Make a test to check for name
    welcome_id = 'Hello Mysterious...'
    if len(name) > 1:
        welcome_id = name
    if len(name) <= 1 and len(email) > 0:
        welcome_id = email
    if len(email) > 1 and len(name) > 1:
        welcome_id = f'{name} : {email}'
    meal_plans = plan.objects.filter(owner=request.user, soft_delete=False)
    context = {'username': user.username,
               'welcome': welcome_id,
               'plans': meal_plans
               }
    return render(request, 'registration/welcome.html', context=context)


class make_plan(CreateView):
    login_required = True
    model = plan
    fields = ['name']
    success_url = reverse_lazy('welcome')
    template_name_suffix = '_make'

    def form_valid(self, form):
        cook = form.save(commit=False)
        cook.owner = User.objects.get(id=self.request.user.id)
        cook.save()
        return redirect('welcome')


@login_required
def view_plans(request):
    meal_plans = plan.objects.filter(owner=request.user, soft_delete=False)
    context = {'meal_plans': meal_plans}
    template = 'cooks/plan.html'
    return render(request, template, context)


@login_required
def view_plan(request, plan_id, review=None, meal_id=None):
    meal_plans = plan.objects.get(owner=request.user, id=plan_id)
    meals = meal_plans.meals_on_plan.all().values('meal_id', 'meal__title',
                                                  'meal__vegan',
                                                  'meal__vegetarian',
                                                  'meal__meal_time',
                                                  'meal__cooking_time',
                                                  'meal__dish_type',
                                                  'meal__cooking_method',
                                                  'meal__rec_url', 'review',)
    if review:
        if review == 1:
            mstr_recipe.objects.filter(meal_id=meal_id).update(upvote=F('upvote') + 1)
            plan_meal.objects.filter(plan_id=plan_id,
                                     meal_id=meal_id).update(review=1)
        if review == 2:
            mstr_recipe.objects.filter(meal_id=meal_id).update(downvote=F('downvote') + 1)
            plan_meal.objects.filter(plan_id=plan_id,
                                     meal_id=meal_id).update(review=-1)
    context = {'meals': meals, 'plan_view': True, 'mp': meal_plans}
    template = 'meals/showmeals.html'
    return render(request, template, context)


@login_required
def add_to_plan(request, plan_id):
    meal_plan = plan.objects.get(owner=request.user, id=plan_id)
    meals_on_plan = meal_plan.meals_on_plan.all()
    meals = mstr_recipe.objects.exclude(meal_id__in=meals_on_plan.values_list(
                                        'meal_id', flat=True)).defer('found_words')
    search = {}
    for value in ['meal_time', 'cooking_time', 'cooking_method', 'dish_type']:
        try:
            val = request.GET[value]
            if val == '%':
                continue
            else:
                search[f'{value}__exact'] = val
        except:
            continue
    if len(search) > 0:
        meals = meals.filter(**search)
    context = {'meals': meals, 'add_to_plan_view': True, 'mp': meal_plan,
               'meal_time': meal_time_choices, 'dish_type': dish_type_choices,
               'cooking_method': cooking_method_choices,
               'cooking_time': cook_time_choices}
    template = 'meals/showmeals.html'
    return render(request, template, context)

@login_required
def add_meal_to_plan(request, plan_id, meal_id):
    mstr_recipe.objects.filter(meal_id=meal_id).update(times_selected=F('times_selected') + 1)
    plan_meal.objects.create(meal_id=meal_id, plan_id=plan_id)
    return redirect('add_to_plan', plan_id=plan_id)


@login_required
def del_meal_from_plan(request, plan_id, meal_id):
    plan_meal.objects.filter(meal_id=meal_id, plan_id=plan_id).delete()
    mstr_recipe.objects.filter(meal_id=meal_id).update(times_selected=F('times_selected') - 1)
    return redirect('view-plan', plan_id=plan_id)


@login_required
def del_plan(request, plan_id):
    plan.objects.filter(id=plan_id,
                        owner=request.user).update(soft_delete=True)
    return redirect('welcome')

