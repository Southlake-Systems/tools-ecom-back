from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Prefetch

from ..models import Product, ProductImage, ProductPrice
from ..serializers.home_page import HomeProductSerializer


class HomePageView(APIView):

    def get(self, request):

        queryset = Product.objects.all().select_related("price").prefetch_related(
            Prefetch("images", queryset=ProductImage.objects.filter(position=1, quality="LOW"))
        )

        serializer = HomeProductSerializer(queryset, many=True)

        return Response({
            "response": serializer.data
        })