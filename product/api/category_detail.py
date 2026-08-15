from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from ..models.category import Category
from ..serializers.category_serializer import CategorySerializer


class CategoryDetailView(APIView):
    """GET, PUT (update), DELETE for /category/:id/"""

    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        serializer = CategorySerializer(category)
        return Response({"response": serializer.data})

    def put(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        serializer = CategorySerializer(category, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "updated", "category": serializer.data})

        return Response(
            {"errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        category.delete()
        return Response({"message": "deleted"}, status=status.HTTP_200_OK)
