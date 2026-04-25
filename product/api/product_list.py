from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from product.models.product import Product
from ..serializers.product_serializer import ProductSerializer


class ProductPagination(PageNumberPagination):
    page_size = 15

class ProductListView(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        return (
            Product.objects
            .select_related("brand")
            .order_by("-id")
        )
    