from django.urls import path
from . import views as share_views


urlpatterns = [
    path('save/<str:meal_id>', share_views.start_share, name='start-shared'),
    path('', share_views.save_share, name='save-shared'),
    path('view/<int:share_id>', share_views.view_share, name='view-shared'),
    path('post/<int:post_id>', share_views.view_posting, name='view-posting'),
    path('post/', share_views.home_postings, name='home-postings'),
    path('ai/', share_views.recipe_ai_start, name='ai-recipe-start'),
    path('ai/review', share_views.recipe_ai_create, name='ai-recipe-create'),
    path('view/ai/<str:ai_html_id>', share_views.view_ai_recipe, name='view-ai-html')

    ]
