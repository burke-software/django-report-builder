from django.urls import re_path

from .views import run_scheduled_report

urlpatterns = [
    re_path(r'^report/(?P<pk>\d+)/run_scheduled_report/$', run_scheduled_report, name="run_scheduled_report"),
]
