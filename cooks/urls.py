from django.urls import path
from . import views as cook_views


urlpatterns = [
    path('register/', cook_views.register_cook, name='register'),
    path('register/welcome', cook_views.cook_profile, name='welcome'),
    path('makeplan', cook_views.make_plan.as_view(), name='make-plan'),
    path('viewplans', cook_views.view_plans, name='view-plans'),
    path('viewplans/<int:plan_id>', cook_views.view_plan, name='view-plan'),
    ]
