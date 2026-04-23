

from rest_framework import serializers
from ..models.product import Product,ProductImage





class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id","product","original"]

    def create(self, validated_data):
        return ProductImage.objects.create(**validated_data)
