from django.urls import path
from . import views as cook_views


urlpatterns = [
    path('register/', cook_views.register_cook, name='register'),
    path('register/welcome', cook_views.cook_profile, name='welcome'),
    path('makeplan', cook_views.make_plan.as_view(), name='make-plan'),
    path('viewplans', cook_views.view_plans, name='view-plans'),
    path('viewplans/<int:plan_id>', cook_views.view_plan, name='view-plan'),
    path('viewplans/<int:plan_id>/<int:review>/<str:meal_id>', cook_views.view_plan, name='view-plan-vote'),
    path('mod_plan/<int:plan_id>', cook_views.add_to_plan, name='add_to_plan'),
    path('mod_plan/<int:plan_id>/<str:meal_id>', cook_views.add_meal_to_plan, name='add_meal_to_plan'),
    path('del_meal_from_plan/<int:plan_id>/<str:meal_id>', cook_views.del_meal_from_plan, name='del_meal_from_plan'),
    path('del_plan/<int:plan_id>', cook_views.del_plan, name='del_plan')
    ]
