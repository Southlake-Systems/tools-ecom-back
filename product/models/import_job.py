from django.db import models


class ImportJob(models.Model):

    class Status(models.TextChoices):
        PENDING    = "pending",    "Pending"
        PROCESSING = "processing", "Processing"
        DONE       = "done",       "Done"
        FAILED     = "failed",     "Failed"

    file          = models.FileField(upload_to="import_jobs/")
    original_name = models.CharField(max_length=255)
    status        = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    total_rows     = models.IntegerField(default=0)
    rows_processed = models.IntegerField(default=0)
    created_count  = models.IntegerField(default=0)
    updated_count  = models.IntegerField(default=0)
    failed_count   = models.IntegerField(default=0)
    results        = models.JSONField(default=list)
    errors         = models.JSONField(default=list)
    dry_run        = models.BooleanField(default=False)
    created_at     = models.DateTimeField(auto_now_add=True)
    started_at     = models.DateTimeField(null=True, blank=True)
    completed_at   = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"ImportJob #{self.pk} — {self.status} ({self.original_name})"
