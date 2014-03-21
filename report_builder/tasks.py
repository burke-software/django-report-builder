from __future__ import absolute_import

from celery import shared_task
from .views import DownloadXlsxView


@shared_task
def report_builder_async_report_save(report_id, user_id):
    view = DownloadXlsxView()
    view.process_report(report_id, user_id, to_response=False)
