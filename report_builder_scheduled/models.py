from django.conf import settings
from django.db import models
import datetime

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class ScheduledReport(models.Model):
    """ A scheduled report that runs and emails itself to various users on
    a recurring basis. Requires celery. """
    is_active = models.BooleanField(default=True)
    report = models.ForeignKey('report_builder.Report')
    users = models.ManyToManyField(AUTH_USER_MODEL, blank=True)
    other_emails = models.CharField(
        max_length=1000,
        blank=True,
        help_text="comma separated list of emails to send to in addition to users")
    last_run = models.DateTimeField(blank=True, null=True, editable=False)

    def __str__(self):
        return str(self.report)

    def _get_list_of_emails(self):
        emails = list(self.users.exclude(email="").values_list('email', flat=True))
        emails += [x.strip() for x in self.other_emails.split(',') if x != '']
        return emails

    def run_report(self):
        self.report.run_report('xlsx', scheduled=True, email_to=self._get_list_of_emails())
        self.last_run = datetime.datetime.now()
        self.save()
