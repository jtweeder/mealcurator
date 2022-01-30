from django.urls import path
from . import views as cook_views


urlpatterns = [
    path('register/', cook_views.register_cook, name='register'),
    path('register/welcome', cook_views.cook_profile, name='welcome'),
    ]
