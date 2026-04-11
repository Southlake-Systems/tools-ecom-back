from rest_framework import serializers
from ..models import Brand
from product.models.product import Product, ProductPrice



class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = ["mrp", "selling_price", "discount_rate"]

class ProductSerializer(serializers.ModelSerializer):
    price = ProductPriceSerializer(read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price", 
            "image",
        ]



    def get_image(self, obj):
        image = obj.images.first()
        return image.image.url if image else None
