from django.conf.urls.defaults import *
from report_builder import views

urlpatterns = patterns('',
    ('^report/add/$',  views.ReportCreateView.as_view()),
    url('^report/(?P<pk>\d+)/$', views.ReportUpdateView.as_view(),name="report_update_view"),
    url('^report/(?P<pk>\d+)/download_xlsx$',  views.download_xlsx),
    ('^ajax_get_related/$', views.ajax_get_related),
    ('^ajax_get_fields/$', views.ajax_get_fields),
    ('^ajax_preview/$', views.ajax_preview),
)
