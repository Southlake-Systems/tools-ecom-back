
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
    products = serializers.SerializerMethodField()

    class Meta:
        model = HomeSection
        fields = ["id", "title", "order","is_active", "products"]

    def get_products(self, obj):
        count = self.context.get("count", 0)

        qs = obj.sectionproduct_set.all()

        if count:
            qs = qs[:count]

        return HomeProductSerializer(
            [sp.product for sp in qs],
            many=True,
            context=self.context  
        ).data


