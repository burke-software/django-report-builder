from django.conf.urls import patterns, url, include
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework import routers
from .views import ReportSPAView
from .api import views as api_views


router = routers.DefaultRouter()
router.register(r'reports', api_views.ReportViewSet)

urlpatterns = patterns('',
    url(r'^api/', include(router.urls)),
    url(r'^api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/related_fields',  staff_member_required(api_views.RelatedFieldsView.as_view()), name="related_fields"),
    url(r'^api/fields',  staff_member_required(api_views.FieldsView.as_view()), name="fields"),
    url(r'^',  staff_member_required(ReportSPAView.as_view()), name="report_builder"),
)
