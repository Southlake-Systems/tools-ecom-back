from rest_framework import serializers
from ..models.product import Product, ProductPrice, ProductImage
from brands.models import Brand
from .product_serializer import FeatureSerializer,SpecificationSerializer



class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = ["mrp", "selling_price", "discount_rate"]

class BrandSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["name"]

class ProductPageSerializer(serializers.ModelSerializer):
    specification = SpecificationSerializer(many=True,read_only=True)
    features = FeatureSerializer(many=True,read_only=True)
    price = ProductPriceSerializer(read_only=True)
    brand = BrandSerializers(read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "brand",
            "description",
            "model_number",
            "stock",
            "price",
            "category",
            "warranty",
            "features",
            "specification",
            "image"
        ]

    def get_image(self, obj):

        request = self.context.get("request")
        result = []

        for product_image in obj.images.all():
            variant = product_image.variants.filter(quality="MID").first()

            if variant and variant.file:
                url = variant.file.url
            elif product_image.original:
                url = product_image.original.url
            else:
                continue

            if request:
                url = request.build_absolute_uri(url)

            result.append({"id": product_image.id, "url": url})

        return result