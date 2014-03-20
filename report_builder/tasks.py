from __future__ import absolute_import

from celery import shared_task


@shared_task
def report_builder_async_report_save(obj, report, objects_list, title, header, widths):
    obj.async_report_save(report, objects_list, title, header, widths)
