from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import PanelTokenObtainPairSerializer
from .utils import get_role


class PanelLoginView(TokenObtainPairView):
    serializer_class = PanelTokenObtainPairSerializer


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(
            {
                "username": user.username,
                "role": get_role(user),
                "is_superuser": user.is_superuser,
            }
        )
