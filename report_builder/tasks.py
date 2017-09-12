from celery import shared_task
from .models import ScheduledReport


@shared_task
def report_builder_file_async_report_save(report_id, user_id, file_type):
    """ Start a report task """
    from .views import DownloadFileView
    view = DownloadFileView()
    view.process_report(report_id, user_id, file_type, to_response=False)

@shared_task
def report_builder_run_scheduled_report(scheduled_report_id: int, file_type="xlsx"):
    report = ScheduledReport.objects.get(pk=scheduled_report_id)
    report.run_report()