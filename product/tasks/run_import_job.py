from celery import shared_task
from django.utils import timezone

from ..models.import_job import ImportJob
from ..excel.import_engine import parse_file, run_import


@shared_task(bind=True, max_retries=2)
def run_import_job(self, job_id: int):
    try:
        job = ImportJob.objects.get(pk=job_id)
    except ImportJob.DoesNotExist:
        return

    job.status = ImportJob.Status.PROCESSING
    job.started_at = timezone.now()
    job.save(update_fields=["status", "started_at"])

    try:
        with job.file.open("rb") as fh:
            df = parse_file(fh, job.original_name)

        job.total_rows = len(df)
        job.save(update_fields=["total_rows"])

        summary = run_import(df, job=job, dry_run=job.dry_run)

        job.status        = ImportJob.Status.DONE
        job.created_count = summary["created"]
        job.updated_count = summary["updated"]
        job.failed_count  = summary["failed"]
        job.results       = summary["results"]
        job.errors        = summary["errors"]
        job.rows_processed = len(df)
        job.completed_at  = timezone.now()
        job.save()

    except Exception as exc:
        job.status       = ImportJob.Status.FAILED
        job.errors       = [{"error": str(exc)}]
        job.completed_at = timezone.now()
        job.save(update_fields=["status", "errors", "completed_at"])
        raise self.retry(exc=exc, countdown=30)
