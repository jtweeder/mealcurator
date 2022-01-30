from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render
from .models import raw_recipe

# Create your views here.
def index(request):
    return render(request, 'font_style.html', context=None)

class get_recipe(CreateView):
    model = raw_recipe
    fields = ['title', 'rec_url','vegan','vegetarian', 'meal_time', 
              'dish_type', 'cooking_method']
    success_url = 'https://www.google.com'
    
class update_recipe(UpdateView):
    model = raw_recipe
    fields = ['title', 'rec_url','vegan','vegetarian', 'meal_time', 
              'dish_type', 'cooking_method']
    template_name_suffix = '_update'

class delete_recipe(DeleteView):
    model = raw_recipe
    template_name_suffix = '_delete'
