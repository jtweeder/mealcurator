from django.contrib import admin
from .models import change_log, changes, meal_item


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


admin.site.register(change_log, change_logAdmin)
admin.site.register(meal_item, meal_itemAdmin)
admin.site.register(changes, change_logAdmin)
