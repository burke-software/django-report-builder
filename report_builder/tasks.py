from __future__ import absolute_import

from celery import shared_task
from .views import DownloadFileView


@shared_task
def report_builder_file_async_report_save(report_id, user_id, file_type):
    view = DownloadFileView()
    view.process_report(report_id, user_id, file_type, to_response=False)
