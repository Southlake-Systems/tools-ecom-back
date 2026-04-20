from django.contrib import admin
from .models import Brand


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "is_processed", "favourite")
    list_filter = ("is_processed", "favourite")
    search_fields = ("name", "description")
    ordering = ("name",)