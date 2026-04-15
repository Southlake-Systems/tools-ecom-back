from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.create_homepage_serializer import HomeSectionCreateSerializer


class CreateHomeSectionView(APIView):

    def post(self, request):
        serializer = HomeSectionCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=400)