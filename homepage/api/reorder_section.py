from rest_framework.views import APIView
from rest_framework.response import Response

from ..models import HomeSection


class ReorderSections(APIView):

    def patch(self, request):

        items = request.data.get("sections", [])

        for item in items:
            HomeSection.objects.filter(
                id=item["id"]
            ).update(
                order=item["order"]
            )

        return Response({
            "message": "updated"
        })