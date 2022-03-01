from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render
from .models import raw_recipe, mstr_recipe


def index(request):
    return render(request, 'font_style.html', context=None)


class get_recipe(CreateView):
    login_required = True
    model = raw_recipe
    fields = ['title', 'rec_url', 'vegan', 'vegetarian', 'meal_time',
              'dish_type', 'cooking_method', 'protein_type', 'cooking_time']
    success_url = reverse_lazy('get-recipe')


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
