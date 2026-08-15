from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch

from ..models.category import Category
from ..models.product import Product, ProductImage
from ..serializers.product_serializer import ProductSerializer


class CategoryProductsView(APIView):
    """GET all products belonging to a category — /category/:id/products/"""

    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)

        products = Product.objects.filter(
            categories=category
        ).select_related("price", "brand").prefetch_related(
            "specification",
            "features",
            "categories",
            Prefetch("images", queryset=ProductImage.objects.all()),
        )

        serializer = ProductSerializer(products, many=True)

        return Response({"response": serializer.data})
