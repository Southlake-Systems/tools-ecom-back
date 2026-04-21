from celery import shared_task
from django.core.files.base import ContentFile
from PIL import Image
import boto3
from io import BytesIO

from ..models import Brand


@shared_task(bind=True, max_retries=3)
def process_brand_image(self, brand_id):
    try:
        brand = Brand.objects.get(id=brand_id)

        if not brand.image_original:
            return

        # Download from S3
        img = Image.open(brand.image_original)

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        def resize(image, width, quality):
            ratio = width / image.width
            height = int(image.height * ratio)
            resized = image.resize((width, height), Image.LANCZOS)

            buffer = BytesIO()
            resized.save(buffer, format="WEBP", quality=quality)
            return ContentFile(buffer.getvalue())

        medium = resize(img, 800, 75)
        thumb = resize(img, 250, 50)

        # Save back to S3
        brand.image_medium.save(f"{brand.id}_med.webp", medium, save=False)
        brand.image_thumbnail.save(f"{brand.id}_thumb.webp", thumb, save=False)

        brand.is_processed = True
        brand.save()

    except Exception as e:
        raise self.retry(exc=e, countdown=10)