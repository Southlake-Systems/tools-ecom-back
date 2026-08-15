from django.urls import path
from .api.add_product import AddProduct
from .api.generate_product_id import GetProdID
from .excel.product_bulk_upload import BulkUploadProducts
from .api.get_all_product import ProductPageView
from .api.upload_image import BulkUploadProductImages
from .api.product_image_update import ProductImageDetailAPIView
from .api.product_live_search import ProductLiveSearch
from .api.product_search import ProductSearchView
from .api.product_list import ProductListView
from .api.upload_product_image import UploadProductImage
from .api.import_job_views import (
    BulkUploadV2,
    BulkUploadTemplate,
    ImportJobListView,
    ImportJobDetailView,
)
from .api.product_detail import ProductDetailView, ProductManageView
from .api.category_list_create import CategoryListCreateView
from .api.category_detail import CategoryDetailView
from .api.category_products import CategoryProductsView

urlpatterns = [
    path('add/', AddProduct.as_view(), name="add product"),
    path('category/', CategoryListCreateView.as_view(), name="category list create"),
    path('category/<int:category_id>/', CategoryDetailView.as_view(), name="category detail"),
    path('category/<int:category_id>/products/', CategoryProductsView.as_view(), name="category products"),
    path('images/upload/', BulkUploadProductImages.as_view(), name="upload product image"),
    path('get/id', GetProdID.as_view(), name="get product id"),
    path('bulk-upload/', BulkUploadProducts.as_view(), name="bulk-upload"),
    path('bulk-upload/v2/', BulkUploadV2.as_view(), name="bulk-upload-v2"),
    path('bulk-upload/template/', BulkUploadTemplate.as_view(), name="bulk-upload-template"),
    path('import-jobs/', ImportJobListView.as_view(), name="import-job-list"),
    path('import-jobs/<int:pk>/', ImportJobDetailView.as_view(), name="import-job-detail"),
    path('search/live/', ProductLiveSearch.as_view(), name="product live search"),
    path('search/', ProductSearchView.as_view(), name="productsearch"),
    path("product-images/<int:id>/", ProductImageDetailAPIView.as_view()),
    path('<int:product_id>/', ProductManageView.as_view(), name="home-page-view"),
    path('<int:product_id>/details/', ProductDetailView.as_view(), name="product-detail"),
    path('', ProductListView.as_view(), name="product list view"),
    path("image/upload/", UploadProductImage.as_view()),
]

