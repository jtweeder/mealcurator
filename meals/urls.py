from django.urls import path
from meals import views


urlpatterns = [
    path('', views.index, name='index')
]