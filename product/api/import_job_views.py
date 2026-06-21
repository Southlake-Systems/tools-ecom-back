from io import BytesIO

import openpyxl
from django.http import HttpResponse
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.import_job import ImportJob
from ..serializers.import_job_serializer import (
    ImportJobDetailSerializer,
    ImportJobListSerializer,
)
from ..tasks.run_import_job import run_import_job


ALLOWED_EXTENSIONS = (".xlsx", ".xls", ".csv")

TEMPLATE_HEADERS = [
    "name",
    "brand",
    "description",
    "model_number",
    "stock",
    "category",
    "warranty",
    "mrp",
    "selling_price",
    "discount_rate",
    "specification/Weight",
    "specification/Power",
    "specification/Voltage",
    "feature/Portable",
    "feature/Waterproof",
]

TEMPLATE_EXAMPLE_ROW = [
    "Drill Pro 3000",
    "Bosch",
    "Professional drill for heavy-duty use",
    "DP-3000",
    100,
    "Power Tools",
    "1 Year",
    2999.00,
    2499.00,
    16.7,
    "1.5kg",
    "500W",
    "220V",
    "Yes",
    "",
]


class BulkUploadV2(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        file = request.FILES.get("file")

        if not file:
            return Response(
                {"success": False, "message": "Excel file is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not any(file.name.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
            return Response(
                {
                    "success": False,
                    "message": f"Unsupported file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        dry_run_param = request.data.get("dry_run", "false")
        dry_run = str(dry_run_param).lower() in ("true", "1", "yes")

        job = ImportJob.objects.create(
            file=file,
            original_name=file.name,
            dry_run=dry_run,
            status=ImportJob.Status.PENDING,
        )

        run_import_job.delay(job.pk)

        return Response(
            {
                "job_id": job.pk,
                "status": job.status,
                "dry_run": dry_run,
                "message": f"Import queued. Poll /product/import-jobs/{job.pk}/ for status.",
            },
            status=status.HTTP_202_ACCEPTED,
        )


class BulkUploadTemplate(APIView):

    def get(self, request):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Products"
        ws.append(TEMPLATE_HEADERS)
        ws.append(TEMPLATE_EXAMPLE_ROW)

        buf = BytesIO()
        wb.save(buf)
        buf.seek(0)

        response = HttpResponse(
            buf.getvalue(),
            content_type=(
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ),
        )
        response["Content-Disposition"] = (
            'attachment; filename="product_import_template.xlsx"'
        )
        return response


class ImportJobListView(APIView):

    def get(self, request):
        jobs = ImportJob.objects.all()[:50]
        serializer = ImportJobListSerializer(jobs, many=True)
        return Response(serializer.data)


class ImportJobDetailView(APIView):

    def get(self, request, pk):
        try:
            job = ImportJob.objects.get(pk=pk)
        except ImportJob.DoesNotExist:
            return Response(
                {"message": "Import job not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = ImportJobDetailSerializer(job)
        return Response(serializer.data)
