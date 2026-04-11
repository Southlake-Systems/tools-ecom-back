from django.urls import path,include
from .api.add_product import AddProduct
from .api.generate_product_id import GetProdID
from .excel.product_bulk_upload import BulkProductUpload
from .api.get_all_product import HomePageView

urlpatterns = [
    path('add/',AddProduct.as_view(), name="add product"),
    path('get/id',GetProdID.as_view(), name="get product id"),
    path('bulk-upload/',BulkProductUpload.as_view(), name="bulk-upload"),
    path('get/all',HomePageView.as_view(), name="home-page-view"),
    


]

