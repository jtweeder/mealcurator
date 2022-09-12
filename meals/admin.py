from django.contrib import admin

from .models import meal_item


class meal_itemAdmin(admin.ModelAdmin):
    class Meta:
        model = meal_item

admin.site.register(meal_item, meal_itemAdmin)