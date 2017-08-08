from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from material.frontend import urls as frontend_urls

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'', include(frontend_urls)),
    # url(r'^admin/', include(admin.site.urls)),
    # url(r'^report_builder/', include('report_builder.urls'))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
