from django.urls import path,include
from .api.add_product import AddProduct
from .api.generate_product_id import GetProdID
from .excel.product_bulk_upload import BulkUploadProducts
from .api.get_all_product import ProductPageView
from .api.upload_image import BulkUploadProductImages
from .api.product_image_update import ProductImageDetailAPIView

urlpatterns = [
    path('add/',AddProduct.as_view(), name="add product"),
    path('images/upload/',BulkUploadProductImages.as_view(), name="upload product image"),
    path('get/id',GetProdID.as_view(), name="get product id"),
    path('bulk-upload/',BulkUploadProducts.as_view(), name="bulk-upload"),
    path("product-images/<int:id>/",ProductImageDetailAPIView.as_view()),
    path('<int:product_id>/',ProductPageView.as_view(), name="home-page-view"),
    


]

