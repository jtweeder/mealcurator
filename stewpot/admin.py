from django.contrib import admin
from .models import meal_posting, share_meal

# Register your models here.
class meal_postingAdmin(admin.ModelAdmin):
    class meta:
        model = meal_posting
    
class share_mealAdmin(admin.ModelAdmin):
    class meta:
        model = share_meal

admin.site.register(meal_posting, meal_postingAdmin)
admin.site.register(share_meal, share_mealAdmin)