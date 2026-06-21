from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import HomeSection


class DeleteSection(APIView):

    def delete(self, request, section_id):

        deleted_count, _ = HomeSection.objects.filter(
            id=section_id
        ).delete()

        if deleted_count == 0:
            return Response(
                {"message": "Section not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {"message": "Section deleted successfully"},
            status=status.HTTP_200_OK
        )