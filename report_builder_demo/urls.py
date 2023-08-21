from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import re_path

admin.autodiscover()

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^report_builder/', include('report_builder_scheduled.urls')),
    re_path(r'^report_builder/', include('report_builder.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
