from django.contrib import admin
from .models import Product, Specifications, Features, ProductPrice, ProductImage


# Inline for Specifications
class SpecificationsInline(admin.TabularInline):
    model = Specifications
    extra = 1


# Inline for Features
class FeaturesInline(admin.TabularInline):
    model = Features
    extra = 1


# Inline for Product Images
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


# Inline for Product Price (OneToOne)
class ProductPriceInline(admin.StackedInline):
    model = ProductPrice
    extra = 0
    max_num = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "brand", "category", "stock")
    search_fields = ("name", "brand", "model_number")
    list_filter = ("brand", "category")
    
    inlines = [
        ProductPriceInline,
        SpecificationsInline,
        FeaturesInline,
        ProductImageInline
    ]


@admin.register(Specifications)
class SpecificationsAdmin(admin.ModelAdmin):
    list_display = ("name", "product_name", "spec")

    def product_name(self, obj):
        return obj.product.name

    product_name.short_description = "Product Name"

@admin.register(Features)
class FeaturesAdmin(admin.ModelAdmin):
    list_display = ("name", "product")
    search_fields = ("name", "product__name")


@admin.register(ProductPrice)
class ProductPriceAdmin(admin.ModelAdmin):
    list_display = ("product", "mrp", "selling_price", "discount_rate")


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "position", "quality")
    list_filter = ("quality",)