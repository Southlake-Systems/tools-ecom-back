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

        if len(q) < 2:
            return Response([])

        products = (
            Product.objects
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
            .only("id", "name")
            [:10]
        )

        return Response([
            {
                "id": p.id,
                "name": p.name
            }
            for p in products
        ])