from django.urls import path
from meals import views


urlpatterns = [
    path('', views.index, name='index'),
    path('submit', views.get_recipe.as_view(), name='get-recipe'),
    path('browse', views.show_recipe, name='view-recipes'),
]