from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.db.models import Count
from mealcurator import choices
from mealcurator.helperfuncs import check_blank
from .models import raw_recipe, mstr_recipe, changes, mstr_recipe_list, meal_item


def staff_check(user):
    return user.is_staff


def index(request):
    return render(request, 'font_style.html', context=None)


def howto(request):
    return render(request, 'howto.html', context=None)


def about(request):
    return render(request, 'about.html', context=None)


def change_log(request):
    change_list = (changes.objects
                          .values('version', 'change', 'entry_date',
                                  'change_desc', 'version__implemented')
                          .order_by('-version__implemented', 'version',
                                    'change',  'entry_date'))
    context = {'changes': change_list}
    return render(request, 'changelog.html', context=context)


class get_recipe(CreateView):
    login_required = True
    model = raw_recipe
    fields = ['title', 'rec_url', 'vegan', 'vegetarian', 'meal_time',
              'dish_type', 'cooking_method', 'protein_type', 'cooking_time']
    success_url = reverse_lazy('get-recipe')

    def form_valid(self, form):
        raw = form.save(commit=False)
        outcome = raw.pull_mstr()
        if outcome:
            raw.mstr_flag = True
        else:
            raw.error_flag = True
        raw.save()
        return redirect('get-recipe')


class update_recipe(UpdateView):
    login_required = True
    model = raw_recipe
    fields = ['title', 'rec_url', 'vegan', 'vegetarian', 'meal_time',
              'dish_type', 'cooking_method', 'cooking_time']
    template_name_suffix = '_update'


class delete_recipe(DeleteView):
    login_required = True
    model = raw_recipe
    template_name_suffix = '_delete'


def show_recipe(request):
    meals = mstr_recipe.objects.all()
    context = {'meals': meals}
    template = 'meals/showmeals.html'
    return render(request, template, context)


@login_required
@user_passes_test(staff_check)
def mstr_lst(request):
    meals = (mstr_recipe.objects
                        .values('title', 'meal_id')
                        .annotate(num_items=Count('mstr_recipe_list__item'))
                        .order_by('num_items', '-times_selected')
                        .filter(dummy=False)
             )
    context = {'meals': meals}
    template = 'meals/mstr_lst.html'
    return render(request, template, context)

@login_required
@user_passes_test(staff_check)
def mstr_lst_idx(request, meal_id):
    meal = mstr_recipe.objects.values('title', 'rec_url').get(meal_id=meal_id)
    items = (mstr_recipe_list.objects.values('item_id', 'qty',
                                             'uom', 'item__item_name')
                                     .filter(meal_id=meal_id))
    item_search = meal_item.objects.all()                          
    context = {'items': items, 
               'meal': meal,
               'items_search': item_search,
               'uoms': choices.uoms,
               'meal_id': meal_id,
               'idx': True}
    template = 'meals/mstr_lst.html'

    return render(request, template, context)


@login_required
@user_passes_test(staff_check)
def mstr_lst_add(request, meal_id):
    if request.method == 'POST':
        sent_item = request.POST.get('new-item').lower()
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
        try:
            item = meal_item.objects.get(item_name=sent_item)
        except meal_item.DoesNotExist:
            meal_item.objects.create(item_name=sent_item)
            item = meal_item.objects.get(item_name=sent_item)
        mstr_recipe_list.objects.create(meal_id=meal_id,
                                        item=item,
                                        qty=item_qty,
                                        uom=item_uom)

    return redirect('edit-mstr-list', meal_id=meal_id)


@login_required
@user_passes_test(staff_check)
def mstr_lst_del(request, meal_id, item_id):
    mstr_recipe_list.objects.filter(meal_id=meal_id, item_id=item_id).delete()

    return redirect('edit-mstr-list', meal_id=meal_id)
