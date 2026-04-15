


from django.urls import path,include
from .api.get_homepage_view import HomePageView

urlpatterns = [
    path('all/',HomePageView.as_view(),name="home page view")
]