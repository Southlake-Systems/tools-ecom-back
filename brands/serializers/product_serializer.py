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
        product_image = obj.images.first()
        if not product_image:
            return None

        variant = product_image.variants.filter(quality="LOW").first()
        if variant and variant.file:
            url = variant.file.url
        elif product_image.original:
            url = product_image.original.url
        else:
            return None

        request = self.context.get("request")
        if request:
            url = request.build_absolute_uri(url)
        return url
