from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from product.models.product import Product
from rest_framework import status
from ..models import SectionProduct,HomeSection
from ..serializers.create_homepage_serializer import AddProductsToSectionSerializer


class AddProductsToSectionView(APIView):

    def post(self, request):
        data = request.data

        section_id = data.get("section_id")
        product_ids = data.get("product_ids", [])
        print(section_id)
        if not isinstance(product_ids, list) or not product_ids:
            raise ValidationError({"product_ids": "Must be a non-empty list"})

        # Validate section
        section = get_object_or_404(HomeSection, id=section_id)

        # Fetch products
        products = Product.objects.filter(id__in=product_ids)

        found_ids = set(products.values_list("id", flat=True))
        missing_ids = set(product_ids) - found_ids

        if missing_ids:
            raise ValidationError({
                "product_ids": f"Invalid IDs: {list(missing_ids)}"
            })

        # Avoid duplicates (important)
        existing = set(
            SectionProduct.objects.filter(
                section=section,
                product__in=products
            ).values_list("product_id", flat=True)
        )

        new_links = [
            SectionProduct(section=section, product=product)
            for product in products
            if product.id not in existing
        ]

        SectionProduct.objects.bulk_create(new_links)

        return Response({
            "message": "Products linked to section successfully"
    },status=200)