from django.urls import path
from . import views as share_views


urlpatterns = [
    path('save/<str:meal_id>', share_views.start_share, name='start-shared'),
    path('', share_views.save_share, name='save-shared'),
    path('view/<int:share_id>', share_views.view_share, name='view-shared'),
    path('post/<int:post_id>', share_views.view_posting, name='view-posting'),
    path('post/', share_views.home_postings, name='home-postings'),

    ]
