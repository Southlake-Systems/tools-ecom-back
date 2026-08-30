from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Brand
from ..serializers.brand_serializer import BrandSerializers



class GetAllBrands(APIView):

    def get(self,request):

        brand_obj = Brand.objects.all()
        if request.query_params.get("shop") == "true":
            brand_obj = brand_obj.filter(show_on_shop=True)
        serializers = BrandSerializers(brand_obj, many=True,context={"request": request} )
        return(
            Response({
                "response" : serializers.data
            },status=200)
        )

