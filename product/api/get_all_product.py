from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.product_page_serializer import ProductPageSerializer
from ..models.product import Product

from django.shortcuts import get_object_or_404

class ProductPageView(APIView):

    def get(self, request, product_id):

        product = get_object_or_404(Product, id=product_id)

        serializer = ProductPageSerializer(product)

        return Response({
            "response": serializer.data
        })