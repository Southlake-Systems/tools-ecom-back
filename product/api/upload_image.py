from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from ..serializers.image_serializer import ImageSerializer
from ..tasks.process_product_image import process_product_images

class BulkUploadProductImages(APIView):

    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):

        product_id = request.data.get("product")
        print(request.FILES)
        images = request.FILES.getlist("images")

        data = [
            {
                "product": product_id,
                "original": image
            }
            for image in images
        ]

        serializer = ImageSerializer(data=data, many=True)

        if serializer.is_valid():
            serializer.save()
            process_product_images.delay(product_id)
            print(serializer.data)

            return Response({
                "success": True,
                "message": "Images uploaded successfully",
                "count": len(serializer.data),
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)