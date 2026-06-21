from django.db import models

from brands.models import Brand
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=300)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,related_name="products") 
    description = models.TextField(max_length=300,blank=True,default="None",null=True)
    model_number = models.CharField(max_length=200,blank=True,default="None",null=True)
    stock = models.IntegerField(default=0)
    category = models.CharField(max_length=100,default="nill")
    warranty = models.CharField(
    max_length=100,
    default="No Warranty"
)
    thumbnail = models.ForeignKey(
        "ProductImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )


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
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )
    original = models.ImageField(upload_to="products/original/", null=True,blank=True)
    is_processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

class ProductImageVariant(models.Model):
    QUALITY_CHOICES = [
        ("LOW", "low"),
        ("MID", "mid"),
        ("HIGH", "high"),
    ]

    image = models.ForeignKey(
        ProductImage,
        on_delete=models.CASCADE,
        related_name="variants"
    )

    file = models.ImageField(
        upload_to="products/variants/"
    )

    jpg_file = models.ImageField(
        upload_to="products/variants_jpg/",
        null=True,
        blank=True
    )

    quality = models.CharField(
        max_length=10,
        choices=QUALITY_CHOICES
    )