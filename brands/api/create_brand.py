
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from ..serializers.brand_serializer import BrandSerializers
from ..tasks.process_cover_photos import process_brand_image

class CreateNewBrand(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = BrandSerializers(data=request.data)

        if serializer.is_valid():
            brand = serializer.save()
            process_brand_image.delay(brand.id)

            return Response({
                "message": "created brand",
                "brand_id": brand.id
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)