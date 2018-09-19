from django.conf.urls import url
from .views import run_scheduled_report


urlpatterns = [
    url(r'^report/(?P<pk>\d+)/run_scheduled_report/$', run_scheduled_report, name="run_scheduled_report"),
]
