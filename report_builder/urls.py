from django.urls import re_path, include
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework import routers
from . import views
from .api import views as api_views
from django.conf import settings

# Create router with explicit basenames
router = routers.DefaultRouter()
router.register(r'reports', api_views.ReportViewSet, basename='reportbuilder_reports')
router.register(r'report', api_views.ReportNestedViewSet, basename='reportbuilder_report')
router.register(r'formats', api_views.FormatViewSet, basename='reportbuilder_formats')
router.register(r'filterfields', api_views.FilterFieldViewSet, basename='reportbuilder_filterfields')
router.register(r'contenttypes', api_views.ContentTypeViewSet, basename='reportbuilder_contenttypes')

urlpatterns = [
    # Download and action endpoints
    re_path(r'^report/(?P<pk>\d+)/download_file/$', views.DownloadFileView.as_view(), name="report_download_file"),
    re_path(r'^report/(?P<pk>\d+)/download_file/(?P<filetype>.+)/$', views.DownloadFileView.as_view(), name="report_download_file_typed"),
    re_path(r'^report/(?P<pk>\d+)/check_status/(?P<task_id>.+)/$', views.check_status, name="report_check_status"),
    re_path(r'^report/(?P<pk>\d+)/add_star/$', views.ajax_add_star, name="ajax_add_star"),
    re_path(r'^report/(?P<pk>\d+)/create_copy/$', views.create_copy, name="report_builder_create_copy"),
    re_path(r'^export_to_report/$', views.ExportToReport.as_view(), name="export_to_report"),
    
    # API endpoints
    re_path(r'^api/', include(router.urls)),
    re_path(r'^api/config/', api_views.ConfigView.as_view(), name='report_builder_api_config'),
    re_path(r'^api/related_fields', staff_member_required(api_views.RelatedFieldsView.as_view()), name="related_fields"),
    re_path(r'^api/fields', staff_member_required(api_views.FieldsView.as_view()), name="fields"),
    re_path(r'^api/report/(?P<report_id>\w+)/generate/', staff_member_required(api_views.GenerateReport.as_view()), name="generate_report"),
    re_path(r'^api/report/(?P<pk>\d+)/download_file/(?P<filetype>.+)/$', views.DownloadFileView.as_view(), name="api_report_download_file"),
    re_path(r'^api/report/(?P<pk>\d+)/check_status/(?P<task_id>.+)/$', views.check_status, name="api_report_check_status"),
    
    # SPA views - MUST come last to avoid conflicts
    re_path(r'^report/(?P<pk>\d+)/$', views.ReportSPAView.as_view(), name="report_update_view"),
]

# Root report builder view
if not hasattr(settings, 'REPORT_BUILDER_FRONTEND') or settings.REPORT_BUILDER_FRONTEND:
    urlpatterns += [
        re_path(r'^$', staff_member_required(views.ReportSPAView.as_view()), name="report_builder"),
    ]
