from rest_framework import serializers

from ..models.category import Category


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "product_count"]
        extra_kwargs = {
            "name": {"required": True},
        }

    def get_product_count(self, obj):
        return obj.products.count()
