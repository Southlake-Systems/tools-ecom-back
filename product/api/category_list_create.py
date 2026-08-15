from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models.category import Category
from ..serializers.category_serializer import CategorySerializer


class CategoryListCreateView(APIView):
    """GET all categories, POST to create a new category."""

    def get(self, request):
        categories = Category.objects.all().order_by("name")
        serializer = CategorySerializer(categories, many=True)
        return Response({"response": serializer.data})

    def post(self, request):
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            category = serializer.save()
            return Response(
                {
                    "message": "created",
                    "category": CategorySerializer(category).data,
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {"errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
