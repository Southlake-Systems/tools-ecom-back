# brands/api/get_brand.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import Brand
from ..serializers.brand_serializer import BrandSerializers


class GetBrand(APIView):

    def get(self, request, brand_id):
        try:
            brand = Brand.objects.get(id=brand_id)

            serializer = BrandSerializers(
                brand,
                context={"request": request}
            )

            return Response(serializer.data)

        except Brand.DoesNotExist:
            return Response(
                {"error": "Brand not found"},
                status=status.HTTP_404_NOT_FOUND
            )