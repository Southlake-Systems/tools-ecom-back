from django.db import models

# Create your models here.
from product.models.product import Product

class HomeSection(models.Model):
    title = models.CharField(max_length=100)  # "On Sale"
    order = models.IntegerField(default=0)

class SectionProduct(models.Model):
    section = models.ForeignKey(HomeSection, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)