from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from rest_framework.response import Response


from ..serializers.product_serializer import ProductSerializer
from ..models import Brand
from product.models.product import Product,ProductPrice,ProductImage


class GetProdByBrand(APIView):



    def post(self,request,brand_id):

        brand_obj = get_object_or_404(Brand,id=brand_id)
        print(brand_obj)

        product = Product.objects.filter(brand=brand_obj).select_related("price").prefetch_related(
            Prefetch("images", queryset=ProductImage.objects.filter(position=1, quality="LOW"))
        )

        serializer = ProductSerializer(product, many=True)


        return Response({
            "response": serializer.data
        })




