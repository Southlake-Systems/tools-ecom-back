
from rest_framework import serializers
from ..models import SectionProduct,HomeSection
from product.serializers.home_page import HomeProductSerializer


class SectionProductSerializer(serializers.ModelSerializer):
    product = HomeProductSerializer()

    class Meta:
        model = SectionProduct
        fields = ["product"]

    def to_representation(self, instance):
        return HomeProductSerializer(instance.product).data



class HomeSectionSerializer(serializers.ModelSerializer):
    products = SectionProductSerializer(
        source="sectionproduct_set", many=True
    )

    class Meta:
        model = HomeSection
        fields = ["id", "title", "order", "products"]