from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import MeView, PanelLoginView

urlpatterns = [
    path("login/", PanelLoginView.as_view(), name="panel-login"),
    path("refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("me/", MeView.as_view(), name="panel-me"),
]
