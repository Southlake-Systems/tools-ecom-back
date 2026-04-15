from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import HomeSection
from ..serializers.homepage_serializer import HomeSectionSerializer


class HomePageView(APIView):

    def get(self, request):
        sections = HomeSection.objects.all().order_by("order")
        serializer = HomeSectionSerializer(sections, many=True)
        return Response(serializer.data)