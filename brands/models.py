from django.db import models




class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to="brands/")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
