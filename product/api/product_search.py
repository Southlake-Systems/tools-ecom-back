from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
)

from ..models.product import Product
from ..serializers.product_serializer import ProductSerializer


class ProductSearchView(APIView):

    def get(self, request):

        q = request.GET.get("q", "").strip()

        if not q:
            return Response({
                "results": []
            })

        vector = (
            SearchVector("name", weight="A") +
            SearchVector("brand__name", weight="B") +
            SearchVector("description", weight="C")
        )

        query = SearchQuery(q)

        products = (
            Product.objects
            .annotate(
                rank=SearchRank(vector, query)
            )
            .filter(rank__gte=0.1)  
            .select_related("brand")
            .prefetch_related("images")
            .order_by("-rank")[:20]
        )

        serializer = ProductSerializer(products, many=True)

        return Response({
            "count": len(serializer.data),
            "results": serializer.data
        })