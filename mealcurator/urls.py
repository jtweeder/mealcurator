from django.contrib import admin
from django.conf.urls import include
from django.urls import path


urlpatterns = [
    path('', include('meals.urls')),
    path('recipe/', include('meals.urls')),
    path('admin/', admin.site.urls),
    path('register/', include('cooks.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('cooks/', include('cooks.urls')),
]
