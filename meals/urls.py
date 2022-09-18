from django.urls import path
from meals import views


urlpatterns = [
    path('', views.index, name='index'),
    path('submit', views.get_recipe.as_view(), name='get-recipe'),
    path('browse', views.show_recipe, name='view-recipes'),
    path('howto', views.howto, name='howto'),
    path('about', views.about, name='about'),
    path('changelog', views.change_log', name='change_log'),
]