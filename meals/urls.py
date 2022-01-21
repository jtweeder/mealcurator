from django.urls import path
from meals import views


urlpatterns = [
    path('', views.index, name='index'),
    path('recipe/submit/', views.get_recipe.as_view(), name='get-recipe')
]