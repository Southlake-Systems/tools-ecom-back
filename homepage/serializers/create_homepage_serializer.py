from rest_framework import serializers
from ..models import HomeSection


class HomeSectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeSection
        fields = ["id", "title", "order"]



from ..models import SectionProduct


class AddProductsToSectionSerializer(serializers.Serializer):
    section_id = serializers.IntegerField()
    product_ids = serializers.ListField(
        child=serializers.IntegerField()
    )

    def create(self, validated_data):
        section_id = validated_data["section_id"]
        product_ids = validated_data["product_ids"]

        objs = [
            SectionProduct(section_id=section_id, product_id=pid)
            for pid in product_ids
        ]

        SectionProduct.objects.bulk_create(objs)
        return {"status": "products added"}