from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import Brand


class DeleteBrand(APIView):

    def delete(self, request, brand_id):
        try:
            brand = Brand.objects.get(id=brand_id)
        except Brand.DoesNotExist:
            return Response(
                {"error": "Brand not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        brand.delete()

        return Response(
            {"message": "Brand deleted"},
            status=status.HTTP_200_OK
        )