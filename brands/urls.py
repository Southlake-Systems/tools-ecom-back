from django.urls import path,include
from .api.get_product import GetProdByBrand



urlpatterns = [
    path('<int:brand_id>/product/',GetProdByBrand.as_view(), name="get product by"),
    


]