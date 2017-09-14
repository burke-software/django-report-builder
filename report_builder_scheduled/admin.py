from django.contrib import admin
from django.core.urlresolvers import reverse
from .models import ScheduledReport


@admin.register(ScheduledReport)
class ScheduledReportAdmin(admin.ModelAdmin):
    list_display = ('report', 'is_active', 'last_run', 'run_report_url')
    list_filter = ('is_active', 'last_run')
    readonly_fields = ('last_run',)

    def run_report_url(self, obj):
        url = reverse('run_scheduled_report', kwargs={'pk': obj.id})
        return '<a href="%s">Run</a>' % (url,)

    run_report_url.allow_tags = True
    run_report_url.short_description = ''
