from django.db import models




class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image_original = models.ImageField(upload_to="brands/original/", null=True, blank=True)
    image_medium = models.ImageField(upload_to="brands/medium/", null=True, blank=True)
    image_thumbnail = models.ImageField(upload_to="brands/thumbnail/", null=True, blank=True)
    is_processed = models.BooleanField(default=False)
    favourite = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name