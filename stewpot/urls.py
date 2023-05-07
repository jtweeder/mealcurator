from django.urls import path
from . import views as share_views


urlpatterns = [
    path('save/<str:meal_id>', share_views.start_share, name='start-shared'),
    path('', share_views.save_share, name='save-shared'),
    path('view/<int:share_id>', share_views.view_share, name='view-shared'),
    ]
