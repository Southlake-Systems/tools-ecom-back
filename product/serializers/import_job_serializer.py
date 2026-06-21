from rest_framework import serializers
from ..models.import_job import ImportJob


class ImportJobListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportJob
        fields = [
            "id",
            "original_name",
            "status",
            "total_rows",
            "rows_processed",
            "created_count",
            "updated_count",
            "failed_count",
            "dry_run",
            "created_at",
            "started_at",
            "completed_at",
        ]


class ImportJobDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportJob
        fields = [
            "id",
            "original_name",
            "status",
            "total_rows",
            "rows_processed",
            "created_count",
            "updated_count",
            "failed_count",
            "dry_run",
            "results",
            "errors",
            "created_at",
            "started_at",
            "completed_at",
        ]
