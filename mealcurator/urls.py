from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap

sitemaps = {'static': StaticViewSitemap}

urlpatterns = [
    path('', include('meals.urls')),
    path('meals/', include('meals.urls')),
    path('admin/', admin.site.urls),
    path('register/', include('cooks.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('cooks/', include('cooks.urls')),
    path('share/', include('stewpot.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
]
