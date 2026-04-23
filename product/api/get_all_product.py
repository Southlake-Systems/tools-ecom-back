from rest_framework.views import APIView
from rest_framework.response import Response


class HomePageView(APIView):

    def get(self, request):


        serializer = "Not in use anymore"

        return Response({
            "response": serializer
        })