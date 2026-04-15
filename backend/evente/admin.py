from .models import EventeFooter
from django.contrib import admin


@admin.register(EventeFooter)
class EventeFooterAdmin(admin.ModelAdmin):
    pass
