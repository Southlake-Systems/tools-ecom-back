from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from ..models import HomeSection, SectionProduct
from product.models.product import Product


class UpdateSection(APIView):

    def patch(self, request, section_id):
        try:
            section = HomeSection.objects.get(id=section_id)
        except HomeSection.DoesNotExist:
            return Response({"message": "section not found"}, status=404)

        data = request.data

        # --- update simple fields ---
        if "title" in data:
            section.title = data["title"]

        if "order" in data:
            section.order = data["order"]

        section.save()

        # --- update products (if provided) ---
        if "product_ids" in data:
            product_ids = data["product_ids"]

            with transaction.atomic():
                # remove old mappings
                SectionProduct.objects.filter(section=section).delete()

                # bulk insert new mappings (FAST)
                products = Product.objects.filter(id__in=product_ids)

                SectionProduct.objects.bulk_create([
                    SectionProduct(section=section, product=p)
                    for p in products
                ])

        return Response({"message": "section updated successfully"}, status=200)