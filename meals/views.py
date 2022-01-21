from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render
from .models import raw_recipe

# Create your views here.
def index(request):
    return render(request, 'meals/font_style.html', context=None)
'''
def get_recipe_2(request):
    if request.method == 'POST':
        form = raw_recipe_form(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('https://mealcurator.azurewebsites.net')
    else:
        form = raw_recipe_form()
    return render(request, 'submission.html', {'form': form})
'''
class get_recipe(CreateView):
    model = raw_recipe
    fields = ['title', 'rec_url','vegan','vegetarian', 'meal_time', 
              'dish_type', 'cooking_method']
    success_url = 'https://www.google.com'
    
class update_recipe(UpdateView):
    model = raw_recipe
    fields = ['title', 'rec_url','vegan','vegetarian', 'meal_time', 
              'dish_type', 'cooking_method']

class delete_recipe(DeleteView):
    model = raw_recipe

    






