from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.db.models import F, Sum, Max, Case, When, Value
from django.views.generic.edit import CreateView
from django.contrib.postgres.search import SearchQuery, SearchRank
from cooks.models import plan, plan_meal, plan_list
from meals.models import meal_item, mstr_recipe, mstr_recipe_list
from mealcurator import choices
from mealcurator.helperfuncs import check_blank
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
        dummy_plan = plan_meal.objects.create(
                        meal_id=mstr_recipe.objects.get(dummy=True).meal_id,
                        plan_id=cook.id)
        plan_list.objects.create(owner=cook.owner, plan_id=cook.id,
                                 meal_id=dummy_plan.meal_id, item_id=1)
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
                                                  'meal__protein_type',
                                                  'meal__rec_url',
                                                  'meal__dummy',
                                                  'review',)
    if review:
        cur_review = plan_meal.objects.get(meal_id=meal_id,
                                           plan_id=plan_id).review
        if review == 1:
            if cur_review == -1:
                mstr_recipe.objects.filter(meal_id=meal_id).update(downvote=F('downvote') - 1,
                                                                   upvote=F('upvote') + 1)
            else:
                mstr_recipe.objects.filter(meal_id=meal_id).update(upvote=F('upvote') + 1)
            plan_meal.objects.filter(plan_id=plan_id,
                                     meal_id=meal_id).update(review=1)
        if review == 2:
            if cur_review == 1:
                mstr_recipe.objects.filter(meal_id=meal_id).update(upvote=F('upvote') - 1,
                                                                   downvote=F('downvote') + 1)
            else:
                mstr_recipe.objects.filter(meal_id=meal_id).update(downvote=F('downvote') + 1)
            plan_meal.objects.filter(plan_id=plan_id,
                                     meal_id=meal_id).update(review=-1)
    context = {'meals': meals, 'plan_view': True, 'mp': meal_plans}
    if 'viewplans' in request.path_info:
        template = 'meals/showmeals.html'
    else:
        template = 'cooks/list.html'
    return render(request, template, context)


@login_required
def add_to_plan(request, plan_id):
    meal_plan = plan.objects.get(owner=request.user, id=plan_id)
    meals_on_plan = meal_plan.meals_on_plan.all()
    meals = mstr_recipe.objects.exclude(meal_id__in=meals_on_plan.values_list(
                                        'meal_id',
                                        flat=True)).defer('found_words')
    search = {}
    for value in ['meal_time', 'cooking_time', 'cooking_method', 'dish_type', 'protein_type', 'q']:
        try:
            val = request.GET[value]
            if val == '%':
                continue
            elif value == 'q':
                if val == '':
                    continue
                else:
                    query = SearchQuery(val)
            else:
                search[f'{value}__exact'] = val
        except:
            continue

    if len(search) > 0:
        meals = meals.filter(**search)
    if 'query' in locals():
        meals = meals.annotate(rank=SearchRank('mstr_search__search_vector', 
                               query)).filter(mstr_search__search_vector=query).order_by('-rank')
    
    context = {'meals': meals,
               'add_to_plan_view': True,
               'mp': meal_plan,
               'meal_time': choices.meal_time_choices,
               'dish_type': choices.dish_type_choices,
               'cooking_method': choices.cooking_method_choices,
               'cooking_time': choices.cook_time_choices,
               'protein_choices': choices.protein_choices,
               'request': request,
               }
    template = 'meals/showmeals.html'
    return render(request, template, context)


@login_required
def add_meal_to_plan(request, plan_id, meal_id):
    mstr_recipe.objects.filter(meal_id=meal_id).update(times_selected=F('times_selected') + 1)
    plan_meal.objects.create(meal_id=meal_id, plan_id=plan_id)
    mstr_list = mstr_recipe_list.objects.filter(meal_id=meal_id)
    if len(mstr_list) > 0:
        objs = [plan_list(owner=request.user,
                          plan_id=plan_id,
                          meal_id=meal_id,
                          item_id=1)
                ]
        for itm in mstr_list:
            objs.append(plan_list(
                            owner=request.user,
                            plan_id=plan_id,
                            meal_id=meal_id,
                            item=itm.item,
                            qty=itm.qty,
                            uom=itm.uom,
                                )
                        )
        out = plan_list.objects.bulk_create(objs)
    else:
        plan_list.objects.create(owner=request.user, plan_id=plan_id,
                                 meal_id=meal_id, item_id=1)
    return redirect('add_to_plan', plan_id=plan_id)


@login_required
def del_meal_from_plan(request, plan_id, meal_id):
    plan_meal.objects.filter(meal_id=meal_id, plan_id=plan_id).delete()
    plan_list.objects.filter(owner=request.user,
                             plan_id=plan_id, meal_id=meal_id).delete()
    mstr_recipe.objects.filter(meal_id=meal_id).update(times_selected=F('times_selected') - 1)
    return redirect('view-plan', plan_id=plan_id)


@login_required
def del_plan(request, plan_id):
    plan.objects.filter(id=plan_id,
                        owner=request.user).update(soft_delete=True)
    plan_list.objects.filter(owner=request.user, plan_id=plan_id).delete()
    return redirect('welcome')


@xframe_options_sameorigin
@login_required
def list_idx(request, plan_id, shp=0):
    if 'shp_list' in request.path_info:
        shp = 1
    if shp == 0:
        list = (plan_list.objects.values('id', 'item_id', 'item__item_name',
                                         'uom', 'qty', 'meal__meal_id',
                                         'meal__title',
                                         'plan_id')
                                 .filter(owner=request.user, plan_id=plan_id))
        template = 'cooks/listedit.html'
    else:
        template = 'cooks/listshop.html'
        list = (plan_list.objects.values('item_id', 'item__item_name', 'uom',
                                         'item__item_location', 'plan_id')
                         .filter(owner=request.user, plan_id=plan_id)
                         .annotate(total_qty=Sum('qty'),
                                   got=Max(Case(
                                           When(got=True, then=1),
                                           default=Value(0))
                                           )
                                   )
                         .order_by('item__item_location', 'item', 'uom')
                )
    items = meal_item.objects.all()
    context = {'list': list, 'uoms': choices.uoms, 'items_search': items}
    return render(request, template, context)


@login_required
def list_add(request, plan_id, meal_id=None, plan_itm_id=None):
    if request.method == 'POST':
        item_qty = int(check_blank(request.POST.get('item-qty'), 0))
        item_dec = request.POST.get('item-qty-dec')
        item_uom = request.POST.get('item-uom')

        # Dict to look up fraction to decimal
        qty_lu = {'1/8': 0.125,
                  '1/4': 0.25,
                  '1/3': 0.334,
                  '1/2': 0.5,
                  '2/3': 0.667,
                  '3/4': 0.75,
                  }
        if item_dec == '%':
            item_dec = 0
        else:
            item_dec = qty_lu[item_dec]
        item_qty += item_dec
        if plan_itm_id:
            (plan_list.objects.filter(id=plan_itm_id, owner=request.user)
                              .update(qty=item_qty, uom=item_uom)
             )
        elif meal_id:
            sent_item = request.POST.get('new-item').lower()
            try:
                item = meal_item.objects.get(item_name=sent_item)
            except meal_item.DoesNotExist:
                meal_item.objects.create(item_name=sent_item)
                item = meal_item.objects.get(item_name=sent_item)
            plan_list.objects.create(owner=request.user, plan_id=plan_id,
                                     meal_id=meal_id, item=item, qty=item_qty,
                                     uom=item_uom)
    return redirect('list-idx', plan_id=plan_id)


@login_required
def list_del(request, plan_id, id):
    plan_list.objects.filter(id=id, owner=request.user).delete()
    return redirect('list-idx', plan_id=plan_id)


@login_required
def shp_got(request, plan_id, item_id, direction):
    new_val = True
    if direction == 0:
        new_val = False
    plan_list.objects.filter(owner=request.user,
                             plan_id=plan_id,
                             item_id=item_id).update(got=new_val)

    return redirect('list-idx-shp', plan_id, 1)
