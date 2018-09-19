from celery import shared_task
import report_builder_scheduled.models


@shared_task
def report_builder_run_scheduled_report(scheduled_report_id: int):
    report = report_builder_scheduled.models.ScheduledReport.objects.get(pk=scheduled_report_id)
    report.run_report()

@shared_task
def report_builder_check_if_scheduled_report():
    """Run any reports that need run - this will kick off another task for
    the actual reports - so this should always run pretty fast """
    for scheduled in report_builder_scheduled.models.ScheduledReport.objects.filter(is_active=True):
        scheduled.run_from_schedule()