from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import random
import string

from ..models import Product, Specifications


def clean(value):
    if pd.isna(value) or value == "":
        return None
    return str(value).strip()


def generate_product_id(length=10):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))


def generate_unique_product_id():
    for _ in range(5):
        pid = generate_product_id()
        if not Product.objects.filter(id=pid).exists():
            return pid
    raise Exception("Failed to generate unique product ID")


PRODUCT_FIELD_MAP = {
    "Company": "brand",
    "Category": "category",
    "Product Name": "name",
    "Model Number": "model_number",
    "Warranty": "warranty",
}


class BulkProductUpload(APIView):

    def post(self, request):
        file = request.FILES.get("file")

        if not file:
            return Response({"error": "No file uploaded"}, status=400)

        try:
            df = pd.read_excel(file)

            created_count = 0
            errors = []

            for index, row in df.iterrows():
                try:
                    # -------------------------
                    # 1. Product Data
                    # -------------------------
                    product_data = {}

                    for excel_col, model_field in PRODUCT_FIELD_MAP.items():
                        value = clean(row.get(excel_col))
                        if value is not None:
                            product_data[model_field] = value

                    if not product_data.get("name"):
                        raise Exception("Missing product name")

                    product_data["id"] = generate_unique_product_id()
                    product_data["stock"] = 0

                    # -------------------------
                    # 2. Save Product
                    # -------------------------
                    product = Product.objects.create(**product_data)

                    # -------------------------
                    # 3. Specifications
                    # -------------------------
                    specs = []

                    for col in df.columns:
                        if col not in PRODUCT_FIELD_MAP:
                            value = clean(row.get(col))

                            if value is not None:
                                specs.append(
                                    Specifications(
                                        product=product,  # keep if your field name is capitalized
                                        name=col,
                                        spec=value
                                    )
                                )

                    if specs:
                        Specifications.objects.bulk_create(specs)

                    created_count += 1

                except Exception as e:
                    errors.append({
                        "row": int(index) + 2,
                        "error": str(e)
                    })

            return Response({
                "created": created_count,
                "failed": len(errors),
                "errors": errors[:10]
            })

        except Exception as e:
            return Response({"error": str(e)}, status=500)