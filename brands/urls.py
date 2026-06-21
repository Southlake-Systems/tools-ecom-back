from django.urls import path,include

from .api.delete_brand import DeleteBrand
from .api.update_brand import UpdateBrand
from .api.get_product import GetProdByBrand
from .api.get_all_brands import GetAllBrands
from .api.create_brand import CreateNewBrand
from .api.get_brand import GetBrand

urlpatterns = [
    path('new/', CreateNewBrand.as_view(), name='create new brand'),
    path('<int:brand_id>/product/',GetProdByBrand.as_view(), name="get product by"),
    path('all/', GetAllBrands.as_view(), name='get all brands'),
    path("<int:brand_id>/update/", UpdateBrand.as_view()),
    path("<int:brand_id>/delete/", DeleteBrand.as_view()),
    path("<int:brand_id>/", GetBrand.as_view()),

]