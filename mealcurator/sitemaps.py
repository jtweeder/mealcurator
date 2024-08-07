from django.contrib import sitemaps
from django.urls import reverse
from stewpot.models import meal_posting, ai_html


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['index', 'get-recipe', 'about', 'howto', 'change_log', 'ccc', 'home-postings']

    def location(self, item):
        return reverse(item)

class BlogSitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.2

    def items(self):
        return meal_posting.objects.all()

    def lastmod(self, obj):
        return obj.created_on
   
    def location(self, obj):
        return f'/share/post/{obj.id}'
    
class AIRecipesSitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.3

    def items(self):
        return ai_html.objects.all()

    def lastmod(self, obj):
        return obj.created_on
    
    def location(self, obj):
        return f'/share/view/ai/{obj.html_id}'

