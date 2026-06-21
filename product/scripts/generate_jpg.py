from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

from product.models.product import ProductImageVariant

variants = ProductImageVariant.objects.all()

for variant in variants:

    if variant.jpg_file:
        continue

    try:
        img = Image.open(variant.file)

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        buffer = BytesIO()

        img.save(
            buffer,
            format="JPEG",
            quality=90,
            optimize=True
        )

        buffer.seek(0)

        jpg_name = variant.file.name.replace(
            ".webp",
            ".jpg"
        )

        variant.jpg_file.save(
            jpg_name,
            ContentFile(buffer.getvalue()),
            save=True
        )

        print("DONE:", jpg_name)

    except Exception as e:
        print("FAILED:", variant.id, e)
