from django.urls import path
from meals import views


urlpatterns = [
    path('', views.index, name='index'),
    path('submit', views.get_recipe.as_view(), name='get-recipe'),
    path('browse', views.show_recipe, name='view-recipes'),
    path('howto', views.howto, name='howto'),
    path('about', views.about, name='about'),
    path('changelog', views.change_log, name='change_log'),
    path('mstr', views.mstr_lst, name='view-mstr-list'),
    path('mstr/<str:meal_id>', views.mstr_lst_idx, name='edit-mstr-list'),
    path('mstr/<str:meal_id>/add', views.mstr_lst_add, name='add-list-item-meal'),
    path('mstr/<str:meal_id>/<int:item_id>', views.mstr_lst_del,
         name='del-list-item-meal'),
]