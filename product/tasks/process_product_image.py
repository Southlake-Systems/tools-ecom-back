from celery import shared_task
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
import os

from ..models.product import ProductImage, ProductImageVariant


@shared_task(bind=True, max_retries=3)
def process_product_images(self, product_id):
    try:

        product_images = ProductImage.objects.filter(
            product_id=product_id,
            is_processed=False
        )

        if not product_images.exists():
            return "No unprocessed images found"

        QUALITY_CONFIG = {
            "LOW": {
                "width": 300,
                "quality": 40,
            },
            "MID": {
                "width": 800,
                "quality": 70,
            },
            "HIGH": {
                "width": 1400,
                "quality": 90,
            },
        }

        for product_image in product_images:

            if not product_image.original:
                continue

            # Open original image from S3
            img = Image.open(product_image.original)

            # Convert to RGB for WEBP compatibility
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            for quality_name, config in QUALITY_CONFIG.items():

                width = config["width"]
                quality = config["quality"]

                # Resize image
                ratio = width / img.width
                height = int(img.height * ratio)

                resized = img.resize((width, height), Image.LANCZOS)

                # Save to buffer
                buffer = BytesIO()

                resized.save(
                    buffer,
                    format="JPEG",
                    quality=quality,
                    optimize=True
                )

                buffer.seek(0)

                # Generate filename
                original_name = os.path.splitext(
                    os.path.basename(product_image.original.name)
                )[0]

                filename = (
                    f"product_{product_image.product.id}/"
                    f"{quality_name.lower()}/"
                    f"{original_name}.jpg"
                )

                # Create variant object
                variant = ProductImageVariant(
                    image=product_image,
                    quality=quality_name
                )

                variant.file.save(
                    filename,
                    ContentFile(buffer.getvalue()),
                    save=True
                )

            # Mark original image as processed
            product_image.is_processed = True
            product_image.save(update_fields=["is_processed"])

        return "Product images processed successfully"

    except Exception as e:
        raise self.retry(exc=e, countdown=10)