# homepage/api/get_section_products.py
from rest_framework.views import APIView
from rest_framework.response import Response

from ..models import HomeSection
from ..serializers.homepage_serializer import HomeSectionSerializer


class GetSectionProducts(APIView):

    def get(self, request, section_id):
        section = HomeSection.objects.get(id=section_id)

        serializer = HomeSectionSerializer(
            section,
            context={"request": request}
        )

        return Response(serializer.data)