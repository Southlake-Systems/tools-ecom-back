from django.contrib import admin
from .models import HomeSection, SectionProduct


# 🔹 Inline: add products inside section
class SectionProductInline(admin.TabularInline):
    model = SectionProduct
    extra = 1


# 🔹 HomeSection Admin
class HomeSectionAdmin(admin.ModelAdmin):
    list_display = ["title", "order"]
    ordering = ["order"]
    inlines = [SectionProductInline]


# 🔹 SectionProduct Admin (optional)
class SectionProductAdmin(admin.ModelAdmin):
    list_display = ["section", "product"]
    list_filter = ["section"]


# ✅ Register only your app models
admin.site.register(HomeSection, HomeSectionAdmin)
admin.site.register(SectionProduct, SectionProductAdmin)