from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models.product import Product
from ..serializers.product_serializer import ProductSerializer
from ..serializers.product_page_serializer import ProductPageSerializer


class ProductManageView(APIView):
    """GET (page view), PUT (update), DELETE for /products/:id/"""

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductPageSerializer(product, context={"request": request})
        return Response({"response": serializer.data})

    def put(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        data = request.data.get("product", request.data)

        serializer = ProductSerializer(product, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "updated", "product_id": product.id})

        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        return Response({"message": "deleted"}, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    """GET /products/:id/details/ — returns editable product fields"""

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductPageSerializer(product, context={"request": request})
        return Response({"product": serializer.data})
