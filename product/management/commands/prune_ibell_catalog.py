import json

from django.core.management.base import BaseCommand
from django.db import transaction

from brands.models import Brand
from product.models.product import Product


class Command(BaseCommand):
    help = "Delete iBELL products whose name is not present in the ibell_products.json catalog."

    def add_arguments(self, parser):
        parser.add_argument(
            "--json",
            default="/home/das/Downloads/ibell_products.json",
            help="Path to the ibell_products.json file.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="List what would be deleted without deleting anything.",
        )

    def handle(self, *args, **options):
        json_path = options["json"]
        dry_run = options["dry_run"]

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        data.pop("meta", None)

        valid_names = set()
        for subcats in data.values():
            for info in subcats.values():
                for entry in info.get("products", []):
                    name = (entry.get("name") or "").strip().lower()
                    if name:
                        valid_names.add(name)

        try:
            brand = Brand.objects.get(name__iexact="iBELL")
        except Brand.DoesNotExist:
            self.stdout.write(self.style.WARNING("No iBELL brand found."))
            return

        to_delete = [
            p for p in Product.objects.filter(brand=brand)
            if p.name.strip().lower() not in valid_names
        ]

        self.stdout.write(f"{len(to_delete)} product(s) to delete:")
        for p in to_delete:
            self.stdout.write(f"  - [{p.id}] {p.name}")

        if dry_run:
            self.stdout.write(self.style.WARNING("Dry run: nothing deleted."))
            return

        with transaction.atomic():
            for p in to_delete:
                p.delete()

        self.stdout.write(self.style.SUCCESS(f"Deleted {len(to_delete)} product(s)."))
