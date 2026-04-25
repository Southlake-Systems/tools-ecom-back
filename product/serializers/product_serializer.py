from rest_framework import serializers
from ..models.product import Product, Specifications, Features


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specifications
        fields = ["id", "name", "spec"]


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Features
        fields = ["id", "name"]


class ProductSerializer(serializers.ModelSerializer):

    specifications = SpecificationSerializer(
        source="specification",
        many=True
    )

    features = FeatureSerializer(
        many=True
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "brand",
            "description",
            "model_number",
            "stock",
            "category",
            "warranty",
            "features",
            "specifications",
        ]

    def create(self, validated_data):

        specifications_data = validated_data.pop("specification", [])
        features_data = validated_data.pop("features", [])

        product = Product.objects.create(**validated_data)

        for spec in specifications_data:
            Specifications.objects.create(
                product=product,
                **spec
            )

        for feature in features_data:
            Features.objects.create(
                product=product,
                **feature
            )

        return product

    def update(self, instance, validated_data):

        specifications_data = validated_data.pop("specification", None)
        features_data = validated_data.pop("features", None)

        # update product fields
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        # replace specifications
        if specifications_data is not None:
            instance.specification.all().delete()

            for spec in specifications_data:
                Specifications.objects.create(
                    product=instance,
                    **spec
                )

        # replace features
        if features_data is not None:
            instance.features.all().delete()

            for feature in features_data:
                Features.objects.create(
                    product=instance,
                    **feature
                )

        return instance