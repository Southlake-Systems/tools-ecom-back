import json
import os
import re
from decimal import Decimal, InvalidOperation

from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from brands.models import Brand
from product.models.category import Category
from product.models.product import Product, ProductImage, ProductPrice


class _DryRunRollback(Exception):
    pass


def slugify(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9.\-]", "_", name)


def normalize(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def parse_price(raw: str) -> Decimal:
    cleaned = re.sub(r"[^0-9.]", "", raw or "")
    try:
        return Decimal(cleaned)
    except InvalidOperation:
        return Decimal("0")


class Command(BaseCommand):
    help = "Import the iBell product catalog (JSON + local photos) into the DB."

    def add_arguments(self, parser):
        parser.add_argument(
            "--json",
            default="/home/das/Downloads/ibell_products.json",
            help="Path to the ibell_products.json file.",
        )
        parser.add_argument(
            "--photos",
            default="/home/das/Downloads/ibell_photos",
            help="Path to the ibell_photos directory.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Run the whole import inside a transaction that is rolled back at the end.",
        )

    def build_image_index(self, photos_dir):
        exact = {}
        fuzzy = {}
        for root, _dirs, files in os.walk(photos_dir):
            for fname in files:
                stem = os.path.splitext(fname)[0]
                path = os.path.join(root, fname)
                exact[stem] = path
                fuzzy[normalize(stem)] = path
        return exact, fuzzy

    def find_image(self, name, exact, fuzzy):
        s = slugify(name)
        if s in exact:
            return exact[s]
        n = normalize(name)
        if n in fuzzy:
            return fuzzy[n]
        return None

    def handle(self, *args, **options):
        json_path = options["json"]
        photos_dir = options["photos"]
        dry_run = options["dry_run"]

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        data.pop("meta", None)

        exact_index, fuzzy_index = self.build_image_index(photos_dir)

        stats = {
            "created": 0,
            "duplicates_tagged": 0,
            "images_matched": 0,
            "images_unmatched": 0,
            "errors": 0,
        }
        unmatched_images = []
        error_rows = []

        try:
            with transaction.atomic():
                self._import_all(
                    data,
                    exact_index,
                    fuzzy_index,
                    dry_run,
                    stats,
                    unmatched_images,
                    error_rows,
                )
        except _DryRunRollback:
            pass

        self.stdout.write(self.style.SUCCESS("Import summary:"))
        for k, v in stats.items():
            self.stdout.write(f"  {k}: {v}")
        if unmatched_images:
            self.stdout.write(self.style.WARNING("Products with no matched image:"))
            for n in unmatched_images:
                self.stdout.write(f"  - {n}")
        if error_rows:
            self.stdout.write(self.style.ERROR("Errors:"))
            for n, e in error_rows:
                self.stdout.write(f"  - {n}: {e}")
        if dry_run:
            self.stdout.write(self.style.WARNING("Dry run: all changes rolled back."))

    def _import_all(
        self, data, exact_index, fuzzy_index, dry_run, stats, unmatched_images, error_rows
    ):
        brand, _ = Brand.objects.get_or_create(
            name__iexact="iBELL", defaults={"name": "iBELL"}
        )

        seen_products = {}
        for category_name, subcats in data.items():
            for subcat_name, info in subcats.items():
                top_category, _ = Category.objects.get_or_create(
                    name__iexact=category_name, defaults={"name": category_name}
                )
                sub_category, _ = Category.objects.get_or_create(
                    name__iexact=subcat_name, defaults={"name": subcat_name}
                )

                for entry in info.get("products", []):
                    name = (entry.get("name") or "").strip()
                    if not name:
                        continue
                    key = name.lower()

                    sp = transaction.savepoint()
                    try:
                        if key in seen_products:
                            product = seen_products[key]
                            product.categories.add(top_category, sub_category)
                            stats["duplicates_tagged"] += 1
                        else:
                            product, created = Product.objects.get_or_create(
                                name=name, brand=brand
                            )
                            product.categories.add(top_category, sub_category)
                            seen_products[key] = product

                            price_exists = ProductPrice.objects.filter(
                                product=product
                            ).exists()
                            if created or not price_exists:
                                price = parse_price(entry.get("price", ""))
                                ProductPrice.objects.update_or_create(
                                    product=product,
                                    defaults={
                                        "mrp": price,
                                        "selling_price": price,
                                        "discount_rate": Decimal("0"),
                                    },
                                )

                            if created or product.thumbnail_id is None:
                                image_path = self.find_image(
                                    name, exact_index, fuzzy_index
                                )
                                if image_path:
                                    with open(image_path, "rb") as img_f:
                                        image = ProductImage(product=product)
                                        image.original.save(
                                            os.path.basename(image_path),
                                            File(img_f),
                                            save=True,
                                        )
                                    product.thumbnail = image
                                    product.save(update_fields=["thumbnail"])
                                    stats["images_matched"] += 1
                                else:
                                    stats["images_unmatched"] += 1
                                    unmatched_images.append(name)

                            if created:
                                stats["created"] += 1

                        transaction.savepoint_commit(sp)
                    except Exception as exc:
                        transaction.savepoint_rollback(sp)
                        stats["errors"] += 1
                        error_rows.append((name, str(exc)))

        if dry_run:
            raise _DryRunRollback()
