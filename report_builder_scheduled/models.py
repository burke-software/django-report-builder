from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import report_builder_scheduled.tasks


AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class ScheduledReport(models.Model):
    """ A scheduled report that runs and emails itself to various users on
    a recurring basis. Requires celery. """
    is_active = models.BooleanField(default=True)
    report = models.ForeignKey(
        'report_builder.Report', on_delete=models.CASCADE
    )
    users = models.ManyToManyField(
            AUTH_USER_MODEL,
            limit_choices_to={'is_staff': True},
            blank=True,
            help_text="Staff users to notify")
    other_emails = models.CharField(
        max_length=1000,
        blank=True,
        help_text="comma separated list of emails to send to in addition to users")
    last_run_at = models.DateTimeField(auto_now_add=True, editable=False)
    interval = models.ForeignKey(
        'django_celery_beat.IntervalSchedule', on_delete=models.CASCADE,
        null=True, blank=True, verbose_name=_('interval'),
    )
    crontab = models.ForeignKey(
        'django_celery_beat.CrontabSchedule', on_delete=models.CASCADE, null=True, blank=True,
        verbose_name=_('crontab'), help_text=_('Use one of interval/crontab'),
    )

    def __str__(self):
        return str(self.report)

    def _get_list_of_emails(self) -> [str]:
        """ Get list of emails for all users to return """
        emails = list(self.users.exclude(email="").values_list('email', flat=True))
        emails += [x.strip() for x in self.other_emails.split(',') if x != '']
        return emails

    def _is_due(self) -> bool:
        """Check if due to run, check against both cron and interval """
        if self.interval:
            is_due, next = self.interval.schedule.is_due(self.last_run_at)
            if is_due:
                return True
        if self.crontab:
            is_due, next = self.crontab.schedule.is_due(self.last_run_at)
            return is_due
        return False

    def run_report(self):
        self.report.run_report('xlsx', scheduled=True, email_to=self._get_list_of_emails())
        self.last_run_at = timezone.now()
        self.save()

    def run_from_schedule(self):
        """Run this only from a celery task - check if report needs to run and
        if so run it as it's own celery task """
        if self._is_due():
            report_builder_scheduled.tasks.report_builder_run_scheduled_report.delay(self.id)
