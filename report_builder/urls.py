from django.conf.urls import patterns, url
from report_builder import views

urlpatterns = patterns('',
    url('^report/add/$',  views.ReportCreateView.as_view(), name="report_create"),
    url('^report/(?P<pk>\d+)/$', views.ReportUpdateView.as_view(), name="report_update_view"),
    url('^report/(?P<pk>\d+)/download_xlsx$',  views.download_xlsx),
    url('^ajax_get_related/$', views.ajax_get_related),
    url('^ajax_get_fields/$', views.ajax_get_fields),
    url('^ajax_get_choices/$', views.ajax_get_choices, name="ajax_get_choices"),
    url('^ajax_get_formats/$', views.ajax_get_formats, name="ajax_get_formats"),
    url('^ajax_preview/$', views.ajax_preview),
    url('^report/(?P<pk>\d+)/add_star/$', views.ajax_add_star),
    url('^report/(?P<pk>\d+)/create_copy/$', views.create_copy),
    url('^export_to_report/$', views.export_to_report),
)
