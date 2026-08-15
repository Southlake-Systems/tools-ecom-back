# product/api/bulk_upload_products.py

import pandas as pd

from django.db import transaction
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from brands.models import Brand
from ..models.product import (
    Product,
    ProductPrice,
    Specifications,
    Features,
)
from ..models.category import Category


class BulkUploadProducts(APIView):
    parser_classes = [MultiPartParser, FormParser]

    """
    Expected:
    form-data
    key: file
    value: excel file (.xlsx or .xls)

    Example columns:

    name
    brand
    description
    model_number
    stock
    category
    warranty

    mrp
    selling_price
    discount_rate

    specification/Weight
    specification/Power
    specification/Voltage

    feature/Portable
    feature/Waterproof
    """

    REQUIRED_COLUMNS = ["name", "brand"]

    PRODUCT_FIELDS = {
        "name",
        "description",
        "model_number",
        "stock",
        "warranty",
    }

    def post(self, request):

        excel_file = request.FILES.get("file")

        if not excel_file:
            return Response(
                {
                    "success": False,
                    "message": "Excel file is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            df = pd.read_excel(excel_file)
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": f"Invalid excel file: {str(e)}"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        df.columns = [str(col).strip() for col in df.columns]

        missing_columns = [
            col for col in self.REQUIRED_COLUMNS
            if col not in df.columns
        ]

        if missing_columns:
            return Response(
                {
                    "success": False,
                    "message": f"Missing required columns: {missing_columns}"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        created_products = []
        errors = []

        for index, row in df.iterrows():

            row_number = index + 2  # excel row number

            try:

                name = self.clean_value(row.get("name"))
                brand_name = self.clean_value(row.get("brand"))

                if not name:
                    errors.append({
                        "row": row_number,
                        "error": "Product name is required"
                    })
                    continue

                if not brand_name:
                    errors.append({
                        "row": row_number,
                        "error": "Brand is required"
                    })
                    continue

                brand = Brand.objects.filter(
                    name__iexact=brand_name
                ).first()

                if not brand:
                    errors.append({
                        "row": row_number,
                        "error": f"Brand '{brand_name}' does not exist"
                    })
                    continue

                with transaction.atomic():

                    product_data = {
                        "brand": brand
                    }

                    for field in self.PRODUCT_FIELDS:

                        if field in row:

                            value = self.clean_value(row.get(field))

                            if value is not None:
                                product_data[field] = value

                    product = Product.objects.create(**product_data)

                    # -------------------------
                    # Category
                    # -------------------------

                    category_name = self.clean_value(row.get("category"))

                    if category_name:
                        category, _ = Category.objects.get_or_create(
                            name__iexact=category_name,
                            defaults={"name": category_name}
                        )
                        product.categories.add(category)

                    # -------------------------
                    # Create Product Price
                    # -------------------------

                    mrp = self.clean_value(row.get("mrp"))
                    selling_price = self.clean_value(
                        row.get("selling_price")
                    )
                    discount_rate = self.clean_value(
                        row.get("discount_rate")
                    )

                    if (
                        mrp is not None or
                        selling_price is not None or
                        discount_rate is not None
                    ):
                        ProductPrice.objects.create(
                            product=product,
                            mrp=mrp or 0,
                            selling_price=selling_price or 0,
                            discount_rate=discount_rate or 0,
                        )

                    # -------------------------
                    # Specifications
                    # -------------------------

                    for column in df.columns:

                        if column.startswith("specification/"):

                            spec_name = (
                                column.replace(
                                    "specification/",
                                    ""
                                ).strip()
                            )

                            spec_value = self.clean_value(
                                row.get(column)
                            )

                            if spec_value:

                                Specifications.objects.create(
                                    product=product,
                                    name=spec_name,
                                    spec=str(spec_value)
                                )

                    # -------------------------
                    # Features
                    # -------------------------

                    for column in df.columns:

                        if column.startswith("feature/"):

                            feature_name = (
                                column.replace(
                                    "feature/",
                                    ""
                                ).strip()
                            )

                            feature_value = self.clean_value(
                                row.get(column)
                            )

                            """
                            If column has any value,
                            feature gets added.
                            """

                            if feature_value:

                                Features.objects.create(
                                    product=product,
                                    name=feature_name
                                )

                    created_products.append({
                        "id": product.id,
                        "name": product.name
                    })

            except Exception as e:

                errors.append({
                    "row": row_number,
                    "error": str(e)
                })

        return Response(
            {
                "success": True,
                "created_count": len(created_products),
                "failed_count": len(errors),
                "created_products": created_products,
                "errors": errors,
            },
            status=status.HTTP_201_CREATED
        )

    def clean_value(self, value):

        if pd.isna(value):
            return None

        if isinstance(value, str):
            value = value.strip()

            if value == "":
                return None

        return value