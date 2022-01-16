from django.urls import path
from meals import views


urlpatters = [
    path('', views.index, name='index'),

]