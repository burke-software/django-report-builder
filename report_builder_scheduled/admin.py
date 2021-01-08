from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import ScheduledReport

try:
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse

@admin.register(ScheduledReport)
class ScheduledReportAdmin(admin.ModelAdmin):
    list_display = ('report', 'is_active', 'last_run_at', 'run_report_url')
    list_filter = ('is_active', 'last_run_at')
    readonly_fields = ('last_run_at',)

    def run_report_url(self, obj):
        url = reverse('run_scheduled_report', kwargs={'pk': obj.id})
        return format_html('<a href="{}">Run Report</a>', url)

    run_report_url.allow_tags = True
    run_report_url.short_description = ''
