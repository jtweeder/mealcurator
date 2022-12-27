from django.urls import path
from . import views as cook_views


urlpatterns = [
    path('register/', cook_views.register_cook, name='register'),
    path('register/welcome', cook_views.cook_profile, name='welcome'),
    path('makeplan', cook_views.make_plan.as_view(), name='make-plan'),
    path('viewplans', cook_views.view_plans, name='view-plans'),
    path('viewplans/<int:plan_id>', cook_views.view_plan, name='view-plan'),
    path('viewplans/<int:plan_id>/<int:review>/<str:meal_id>',
         cook_views.view_plan, name='view-plan-vote'),
    path('mod_list/<int:plan_id>', cook_views.view_plan, name='mod-list'),
    path('shp_list/<int:plan_id>', cook_views.list_idx, name='shop-list'),
    path('shp_list/<int:plan_id>/<int:item_id>/<int:direction>',
         cook_views.shp_got, name='chg-list-item'),
    path('idx_list/<int:plan_id>', cook_views.list_idx, name='list-idx'),
    path('idx_list/<int:plan_id>/<int:shp>', cook_views.list_idx, 
         name='list-idx-shp'),
    path('add_list/<int:plan_id>/<str:meal_id>',
         cook_views.list_add, name='add-list-item'),
    path('edit_list/<int:plan_id>/<int:plan_itm_id>',
         cook_views.list_add, name='edit-list-item'),
    path('del_list/<int:plan_id>/<int:id>',
         cook_views.list_del, name='del-list-item'),
    path('mod_plan/<int:plan_id>', cook_views.add_to_plan, name='add_to_plan'),
    path('mod_plan/<int:plan_id>/<str:meal_id>', cook_views.add_meal_to_plan,
         name='add_meal_to_plan'),
    path('del_meal_from_plan/<int:plan_id>/<str:meal_id>',
         cook_views.del_meal_from_plan, name='del_meal_from_plan'),
    path('del_plan/<int:plan_id>', cook_views.del_plan, name='del_plan')
    ]
