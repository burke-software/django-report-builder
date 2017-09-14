from celery import shared_task
from .models import ScheduledReport


@shared_task
def report_builder_run_scheduled_report(scheduled_report_id: int):
    report = ScheduledReport.objects.get(pk=scheduled_report_id)
    report.run_report()
