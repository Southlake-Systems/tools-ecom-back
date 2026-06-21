from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.shortcuts import get_object_or_404

from product.models.product import Product, ProductImage

class UploadProductImage(APIView):

    parser_classes = [MultiPartParser]

    def post(self, request):

        product_id = request.data.get("product_id")
        image = request.FILES.get("images")

        if not product_id:
            return Response({"error": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not image:
            return Response({"error": "images is required"}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, id=product_id)

        product_image = ProductImage.objects.create(
            product=product,
            original=image
        )

        return Response({"message": "uploaded", "id": product_image.id}, status=status.HTTP_201_CREATED)