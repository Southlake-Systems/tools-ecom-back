from rest_framework import serializers
from ..models import Product, ProductPrice, ProductImage

class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = ["mrp", "selling_price", "discount_rate"]


class HomeProductSerializer(serializers.ModelSerializer):
    price = ProductPriceSerializer(read_only=True)
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
        image = obj.images.first()
        return image.image.url if image else None