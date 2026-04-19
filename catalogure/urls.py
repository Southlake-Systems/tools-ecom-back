from django.urls import path
from .views import product_capture_view, save_images

urlpatterns = [
    path('product/capture/', product_capture_view),
    path('product/save-images/', save_images),
]