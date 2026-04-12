from django.urls import path,include
from .api.get_product import GetProdByBrand
from .api.get_all_brands import GetAllBrands


urlpatterns = [
    path('<int:brand_id>/product/',GetProdByBrand.as_view(), name="get product by"),
    path('all/', GetAllBrands.as_view(), name='get all brands'),
    


]