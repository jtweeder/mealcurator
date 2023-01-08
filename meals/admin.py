from django.contrib import admin
from .models import change_log, changes, meal_item, creative_commons


class meal_itemAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'item_location', 'poss_duplicate']
    list_editable = ['item_location', 'poss_duplicate']
    list_display_links = ['item_name']
    list_filter = ['item_location']

    class Meta:
        model = meal_item


class change_logAdmin(admin.ModelAdmin):
    class meta:
        model = change_log


class changes_Admin(admin.ModelAdmin):
    class meta:
        model = changes


class creative_commonsAdmin(admin.ModelAdmin):
    list_display = ['title']

    class meta:
        model = creative_commons


admin.site.register(change_log, change_logAdmin)
admin.site.register(meal_item, meal_itemAdmin)
admin.site.register(changes, change_logAdmin)
admin.site.register(creative_commons, creative_commonsAdmin)
