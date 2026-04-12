
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.brand_serializer import BrandSerializers

class CreateNewBrand(APIView):

    def post(self,request):

        data = request.data.get('brand')
        if not data:
            return Response(
                {"error": "payload is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = BrandSerializers(data=data)

        if serializer.is_valid():
            brand = serializer.save()
            return Response({
                "message": "created brand",
                "brand_id": brand.id
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)