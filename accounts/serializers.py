from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .utils import get_role


class PanelTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = get_role(user)
        token["username"] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["username"] = self.user.username
        data["role"] = get_role(self.user)
        data["is_superuser"] = self.user.is_superuser
        return data
