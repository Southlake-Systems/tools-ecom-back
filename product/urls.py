from django.urls import path,include
from .api.add_product import AddProduct
from .api.generate_product_id import GetProdID

urlpatterns = [
    path('add/',AddProduct.as_view(), name="add product"),
    path('get/id',GetProdID.as_view(), name="get product id"),

]

