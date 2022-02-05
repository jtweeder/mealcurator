from django.contrib import admin

from .models import plan

class planAdmin(admin.ModelAdmin):
    class Meta:
        model = plan

admin.site.register(plan, planAdmin)
