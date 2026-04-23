from rest_framework import serializers
from ..models.product import Product






class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "brand",
            "description",
            "model_number",
            "stock",
        ]

    def create(self, validated_data):
        # called when creating new product
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # called when updating existing product
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance