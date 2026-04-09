import string
import random

from rest_framework.views import APIView
from rest_framework.response import Response




def generate_product_id(length=10):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))


class GetProdID(APIView):

    def get(self,request):
        id = generate_product_id()
        return (
            Response(
                {
                "id" : id
            },status=200
            )
        )