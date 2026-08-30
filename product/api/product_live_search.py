from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.postgres.search import (
    TrigramSimilarity
)
from django.db.models import Q


from ..models.product import Product


class ProductLiveSearch(APIView):

    def get(self, request):

        q = request.GET.get("q", "").strip()
        brand = request.GET.get("brand", "").strip()

        if len(q) < 2 and not brand:
            return Response([])

        products = Product.objects.all()

        if brand:
            products = products.filter(brand_id=brand)

        if len(q) >= 2:
            products = (
                products
                .annotate(
                    similarity=TrigramSimilarity(
                        "name",
                        q
                    )
                )
                .filter(
                    Q(name__icontains=q) |
                    Q(similarity__gt=0.15)
                )
                .order_by("-similarity")
            )
        else:
            products = products.order_by("name")

        limit = 1000 if brand else 10
        products = products.only("id", "name")[:limit]

        return Response([
            {
                "id": p.id,
                "name": p.name
            }
            for p in products
        ])