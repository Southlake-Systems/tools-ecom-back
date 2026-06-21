from rest_framework import serializers
from ..models.product import Product, Specifications, Features, ProductPrice


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specifications
        fields = ["id", "name", "spec"]


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Features
        fields = ["id", "name"]


class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = ["mrp", "selling_price", "discount_rate"]


class ProductSerializer(serializers.ModelSerializer):

    specifications = SpecificationSerializer(
        source="specification",
        many=True,
        required=False
    )

    features = FeatureSerializer(
        many=True,
        required=False
    )

    price = ProductPriceSerializer(required=False, allow_null=True)

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
            "price",
        ]
        extra_kwargs = {
            "brand": {"required": True},
            "name": {"required": True},
        }

    def create(self, validated_data):

        specifications_data = validated_data.pop("specification", [])
        features_data = validated_data.pop("features", [])
        price_data = validated_data.pop("price", None)

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

        if price_data:
            ProductPrice.objects.create(
                product=product,
                **price_data
            )

        return product

    def update(self, instance, validated_data):

        specifications_data = validated_data.pop("specification", None)
        features_data = validated_data.pop("features", None)
        price_data = validated_data.pop("price", None)

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

        # update price
        if price_data is not None:
            ProductPrice.objects.update_or_create(
                product=instance,
                defaults=price_data
            )

        return instance