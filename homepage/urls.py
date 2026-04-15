


from django.urls import path,include
from .api.get_homepage_view import HomePageView
from .api.add_product import AddProductsToSectionView
from .api.create_section import CreateHomeSectionView
urlpatterns = [
    path('all/',HomePageView.as_view(),name="home page view"),
    path("sections/create/", CreateHomeSectionView.as_view()),
    path("sections/add-products/", AddProductsToSectionView.as_view()),
]