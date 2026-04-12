from django.urls import path,include
from .api.get_product import GetProdByBrand
from .api.get_all_brands import GetAllBrands
from .api.create_brand import CreateNewBrand


urlpatterns = [
    path('new/', CreateNewBrand.as_view(), name='create new brand'),
    path('<int:brand_id>/product/',GetProdByBrand.as_view(), name="get product by"),
    path('all/', GetAllBrands.as_view(), name='get all brands'),
    


]