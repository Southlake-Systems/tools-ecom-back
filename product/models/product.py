from django.db import models

from .brands import Brand
# Create your models here.

class Product(models.Model):
    id = models.CharField(max_length=100,primary_key=True)
    name = models.CharField(max_length=300)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,related_name="products") 
    description = models.TextField(max_length=300)
    model_number = models.CharField(max_length=200)
    stock = models.IntegerField(default=0)
    category = models.CharField(max_length=100,default="nill")
    warranty = models.CharField(max_length=10,default=0)

    def __str__(self):
        return self.name


class Specifications(models.Model):
    product = models.ForeignKey( Product, on_delete=models.CASCADE,related_name="specification")
    name = models.CharField(max_length=200)
    spec = models.CharField(max_length=200,default="NILL")
    def __str__(self):
        return self.name
    

class Features(models.Model):
    product = models.ForeignKey( Product, on_delete=models.CASCADE,related_name="features")
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name


class ProductPrice(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="price"
    )
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} Price"


class ProductImage(models.Model):
    QUALITY_CHOICES = [
        ("LOW", "Low Quality"),
        ("HIGH", "High Quality"),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(upload_to="products/")
    
    position = models.IntegerField()  # 1 to 5
    quality = models.CharField(max_length=10, choices=QUALITY_CHOICES)

    class Meta:
        unique_together = ("product", "position", "quality")