from rest_framework import serializers
from ..models.product import Product, ProductPrice, ProductImage
from brands.models import Brand


class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = ["mrp", "selling_price", "discount_rate"]

class BrandSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["name"]

class HomeProductSerializer(serializers.ModelSerializer):
    price = ProductPriceSerializer(read_only=True)
    brand = BrandSerializers(read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "brand",
            "price",
            "image",
        ]

    def get_image(self, obj):

        request = self.context.get("request")

        # first product image
        product_image = obj.images.first()

        if not product_image:
            return None

        # get MID quality variant
        variant = product_image.variants.filter(
            quality="MID"
        ).first()

        # fallback to original image
        if variant and variant.file:
            url = variant.file.url

        elif product_image.original:
            url = product_image.original.url

        else:
            return None

        if request:
            return request.build_absolute_uri(url)

        return url