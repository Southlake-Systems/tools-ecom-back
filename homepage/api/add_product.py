from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.create_homepage_serializer import AddProductsToSectionSerializer


class AddProductsToSectionView(APIView):

    def post(self, request):
        serializer = AddProductsToSectionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Products added successfully"})

        return Response(serializer.errors, status=400)