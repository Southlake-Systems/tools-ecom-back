from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Brand
from ..serializers.brand_serializer import BrandSerializers



class GetAllBrands(APIView):

    def get(self,request):

        brand_obj = Brand.objects.all()
        serializers = BrandSerializers(brand_obj, many=True)
        return(
            Response({
                "response" : serializers.data
            },status=200)
        )

