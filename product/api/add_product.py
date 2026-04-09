from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Product
from ..serializers.product_serializer import ProductSerializer


class AddProduct(APIView):

    def post(self, request):
        data = request.data.get("product")

        if not data:
            return Response(
                {"error": "payload is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # check if product exists
        product_instance = Product.objects.filter(id=data.get("id")).first()

        if product_instance:
            serializer = ProductSerializer(product_instance, data=data)
        else:
            serializer = ProductSerializer(data=data)

        if serializer.is_valid():
            product = serializer.save()
            return Response({
                "message": "created" if not product_instance else "updated",
                "product_id": product.id
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)