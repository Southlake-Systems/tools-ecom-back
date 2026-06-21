from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import Brand
from ..serializers.brand_serializer import BrandSerializers
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
)

class UpdateBrand(APIView):

    parser_classes = (MultiPartParser, FormParser)

    def put(self, request, brand_id):
        try:
            brand = Brand.objects.get(id=brand_id)
        except Brand.DoesNotExist:
            return Response(
                {"error": "Brand not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BrandSerializers(
            brand,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )