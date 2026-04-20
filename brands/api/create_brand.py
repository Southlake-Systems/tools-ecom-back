
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from ..serializers.brand_serializer import BrandSerializers
from django.core.files.storage import default_storage

class CreateNewBrand(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = BrandSerializers(data=request.data)

        if serializer.is_valid():
            brand = serializer.save()
            return Response({
                "message": "created brand",
                "brand_id": brand.id
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)