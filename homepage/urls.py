from django.urls import path,include
from homepage.api.reorder_section import ReorderSections
from .api.get_homepage_view import HomePageView
from .api.add_product import AddProductsToSectionView
from .api.create_section import CreateHomeSectionView
from .api.update_section import UpdateSection
from .api.delete_section import DeleteSection
from .api.get_section_products import GetSectionProducts
urlpatterns = [
    path('all/',HomePageView.as_view(),name="home page view"),
    path("sections/create/", CreateHomeSectionView.as_view()),
    path("sections/add-products/", AddProductsToSectionView.as_view()),
    path("sections/update/<int:section_id>/", UpdateSection.as_view()),
    path("sections/reorder/",ReorderSections.as_view()),
    path("sections/delete/<int:section_id>/",DeleteSection.as_view()),
    path(
    "sections/<int:section_id>/products/",
    GetSectionProducts.as_view()
)
]