import pandas as pd
from django.db import transaction

from brands.models import Brand
from ..models.product import Product, ProductPrice, Specifications, Features
from ..models.import_job import ImportJob


class _DryRunRollback(Exception):
    pass


def parse_file(file_obj, filename: str) -> pd.DataFrame:
    name = filename.lower()
    if name.endswith(".csv"):
        df = pd.read_csv(file_obj)
    else:
        df = pd.read_excel(file_obj)
    df.columns = [str(col).strip() for col in df.columns]
    return df


def _clean(value):
    if pd.isna(value):
        return None
    if isinstance(value, str):
        value = value.strip()
        if value == "":
            return None
    return value


PRODUCT_FIELDS = {"name", "description", "model_number", "stock", "category", "warranty"}


def process_row(row, row_number: int, brand_cache: dict, columns, dry_run: bool = False) -> dict:
    name = _clean(row.get("name"))
    brand_name = _clean(row.get("brand"))

    if not name:
        return {"row": row_number, "status": "error", "product_id": None,
                "name": None, "error": "Product name is required"}

    if not brand_name:
        return {"row": row_number, "status": "error", "product_id": None,
                "name": name, "error": "Brand is required"}

    try:
        sp = transaction.savepoint()

        # Brand — get or auto-create
        if brand_name not in brand_cache:
            brand, _ = Brand.objects.get_or_create(
                name__iexact=brand_name,
                defaults={"name": brand_name},
            )
            brand_cache[brand_name] = brand
        brand = brand_cache[brand_name]

        # Upsert product
        existing = Product.objects.filter(name__iexact=name, brand=brand).first()
        action = "updated" if existing else "created"

        product_data = {"brand": brand}
        for field in PRODUCT_FIELDS:
            if field in row and field != "name":
                val = _clean(row.get(field))
                if val is not None:
                    product_data[field] = val

        if existing:
            for field, val in product_data.items():
                setattr(existing, field, val)
            existing.name = name
            existing.save()
            product = existing
            # Clear old specs and features to recreate them fresh
            product.specification.all().delete()
            product.features.all().delete()
        else:
            product_data["name"] = name
            product = Product.objects.create(**product_data)

        # Price
        mrp           = _clean(row.get("mrp"))
        selling_price = _clean(row.get("selling_price"))
        discount_rate = _clean(row.get("discount_rate"))

        if any(v is not None for v in [mrp, selling_price, discount_rate]):
            ProductPrice.objects.update_or_create(
                product=product,
                defaults={
                    "mrp":           mrp or 0,
                    "selling_price": selling_price or 0,
                    "discount_rate": discount_rate or 0,
                },
            )

        # Specifications
        for col in columns:
            if col.startswith("specification/"):
                spec_name = col.replace("specification/", "").strip()
                spec_value = _clean(row.get(col))
                if spec_value:
                    Specifications.objects.create(
                        product=product,
                        name=spec_name,
                        spec=str(spec_value),
                    )

        # Features
        for col in columns:
            if col.startswith("feature/"):
                feature_name = col.replace("feature/", "").strip()
                feature_value = _clean(row.get(col))
                if feature_value:
                    Features.objects.create(product=product, name=feature_name)

        if dry_run:
            transaction.savepoint_rollback(sp)
            return {"row": row_number, "status": action, "product_id": None,
                    "name": name, "error": None}

        transaction.savepoint_commit(sp)
        return {"row": row_number, "status": action, "product_id": product.pk,
                "name": name, "error": None}

    except Exception as exc:
        try:
            transaction.savepoint_rollback(sp)
        except Exception:
            pass
        return {"row": row_number, "status": "error", "product_id": None,
                "name": name, "error": str(exc)}


def run_import(df: pd.DataFrame, job=None, dry_run: bool = False) -> dict:
    columns = list(df.columns)
    brand_cache: dict = {}
    results = []
    errors = []
    created = updated = failed = 0

    for index, row in df.iterrows():
        row_number = index + 2  # 1-indexed + header row
        outcome = process_row(row, row_number, brand_cache, columns, dry_run=dry_run)

        if outcome["status"] == "created":
            created += 1
            results.append(outcome)
        elif outcome["status"] == "updated":
            updated += 1
            results.append(outcome)
        else:
            failed += 1
            errors.append({"row": outcome["row"], "error": outcome["error"]})

        # Update job progress every 10 rows
        if job is not None and (index + 1) % 10 == 0:
            ImportJob.objects.filter(pk=job.pk).update(rows_processed=index + 1)

    if job is not None:
        ImportJob.objects.filter(pk=job.pk).update(rows_processed=len(df))

    return {
        "created": created,
        "updated": updated,
        "failed":  failed,
        "results": results,
        "errors":  errors,
    }
