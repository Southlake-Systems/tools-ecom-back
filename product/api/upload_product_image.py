from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from product.models.product import Product, ProductImage

class UploadProductImage(APIView):

    parser_classes = [MultiPartParser]

    def post(self, request):

        product_id = request.data.get("product_id")
        image = request.FILES.get("image")

        print("PRODUCT:", product_id)
        print("FILES:", request.FILES)

        product = Product.objects.get(id=product_id)

        ProductImage.objects.create(
            product=product,
            original=image
        )

        return Response({
            "message": "uploaded"
        })