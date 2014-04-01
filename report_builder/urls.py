from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required
from report_builder import views

urlpatterns = patterns('',
    url('^report/add/$',  views.ReportCreateView.as_view(), name="report_create"),
    url('^report/(?P<pk>\d+)/$', views.ReportUpdateView.as_view(), name="report_update_view"),
    url('^report/(?P<pk>\d+)/check_status/(?P<task_id>.+)/$', views.check_status, name="report_check_status"),
    url('^report/(?P<pk>\d+)/download_xlsx/$',  views.DownloadXlsxView.as_view(), name="report_download_xlsx"),
    url('^ajax_get_related/$', staff_member_required(views.AjaxGetRelated.as_view())),
    url('^ajax_get_fields/$', staff_member_required(views.AjaxGetFields.as_view())),
    url('^ajax_get_choices/$', views.ajax_get_choices, name="ajax_get_choices"),
    url('^ajax_get_formats/$', views.ajax_get_formats, name="ajax_get_formats"),
    url('^ajax_preview/$', views.AjaxPreview.as_view()),
    url('^report/(?P<pk>\d+)/add_star/$', views.ajax_add_star),
    url('^report/(?P<pk>\d+)/create_copy/$', views.create_copy),
    url('^export_to_report/$', views.ExportToReport.as_view(), name="export_to_report"),
)
