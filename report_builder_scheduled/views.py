from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .tasks import report_builder_run_scheduled_report
from .models import ScheduledReport

try:
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse

@staff_member_required
def run_scheduled_report(request, pk):
    """ Manually run a scheduled report - useful for testing or one off situations """
    scheduled_report = get_object_or_404(ScheduledReport, pk=pk)
    report_builder_run_scheduled_report.delay(scheduled_report.id)
    messages.success(request, "Ran scheduled report")
    return HttpResponseRedirect(reverse('admin:report_builder_scheduled_scheduledreport_changelist'))
