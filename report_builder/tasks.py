from celery import shared_task


@shared_task
def report_builder_file_async_report_save(report_id, user_id, file_type):
    """ Start a report task """
    from .views import DownloadFileView
    view = DownloadFileView()
    view.process_report(report_id, user_id, file_type, to_response=False)
