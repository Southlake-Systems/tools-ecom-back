# products/admin.py

from django.contrib import admin
from .models import (
    Product,
    Specifications,
    Features,
    ProductPrice,
    ProductImage,
    ProductImageVariant,
)


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


class ProductImageVariantInline(admin.TabularInline):
    model = ProductImageVariant
    extra = 0


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1
    show_change_link = True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "brand",
        "category",
        "stock",
    )

    list_filter = (
        "brand",
        "category",
    )

    search_fields = (
        "name",
        "model_number",
        "brand__name",
    )

    readonly_fields = ()

    inlines = [
        ProductPriceInline,
        SpecificationsInline,
        FeaturesInline,
        ProductImageInline,
    ]

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "name",
                    "brand",
                    "category",
                    "description",
                    "model_number",
                )
            },
        ),
        (
            "Inventory",
            {
                "fields": (
                    "stock",
                    "warranty",
                    "thumbnail",
                )
            },
        ),
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "is_processed",
        "created_at",
    )

    list_filter = (
        "is_processed",
    )

    search_fields = (
        "product__name",
    )

    inlines = [ProductImageVariantInline]


@admin.register(ProductImageVariant)
class ProductImageVariantAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "image",
        "quality",
    )

    list_filter = (
        "quality",
    )


@admin.register(Specifications)
class SpecificationsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "name",
        "spec",
    )

    search_fields = (
        "product__name",
        "name",
    )


@admin.register(Features)
class FeaturesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "name",
    )

    search_fields = (
        "product__name",
        "name",
    )


@admin.register(ProductPrice)
class ProductPriceAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "mrp",
        "selling_price",
        "discount_rate",
    )

    search_fields = (
        "product__name",
    )