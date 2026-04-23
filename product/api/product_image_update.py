# product/api/product_image_detail.py

from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from product.models.product import ProductImage
from product.serializers.image_serializer import ImageSerializer


class ProductImageDetailAPIView(APIView):

    parser_classes = [MultiPartParser, FormParser]

    def patch(self, request, id):

        image = get_object_or_404(ProductImage, id=id)

        serializer = ImageSerializer(
            image,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):

        image = get_object_or_404(ProductImage, id=id)

        image.delete()

        return Response(
            {"message": "Image deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )