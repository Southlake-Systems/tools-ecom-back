from django.contrib import admin
from .models import Product, Specifications, Features, ProductPrice, ProductImage


# --- INLINE MODELS ---

class SpecificationsInline(admin.TabularInline):
    model = Specifications
    extra = 1


class FeaturesInline(admin.TabularInline):
    model = Features
    extra = 1


class ProductPriceInline(admin.StackedInline):
    model = ProductPrice
    extra = 0
    max_num = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


# --- MAIN PRODUCT ADMIN ---

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "brand", "stock")
    search_fields = ("name", "brand", "model_number")
    list_filter = ("brand",)
    
    inlines = [
        ProductPriceInline,
        SpecificationsInline,
        FeaturesInline,
        ProductImageInline
    ]


# --- OPTIONAL: SEPARATE REGISTRATIONS ---

@admin.register(Specifications)
class SpecificationsAdmin(admin.ModelAdmin):
    list_display = ("name", "Product")
    search_fields = ("name",)


@admin.register(Features)
class FeaturesAdmin(admin.ModelAdmin):
    list_display = ("name", "Product")
    search_fields = ("name",)


@admin.register(ProductPrice)
class ProductPriceAdmin(admin.ModelAdmin):
    list_display = ("product", "mrp", "selling_price", "discount_rate")


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "position", "quality")
    list_filter = ("quality",)