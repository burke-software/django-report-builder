from django.contrib.auth import get_user_model
from django.conf import settings
from django.core import mail
from django.test import TestCase
from django.test.utils import override_settings

from model_bakery import baker
from report_builder.tasks import report_builder_file_async_report_save


from ..email import email_report


User = get_user_model()


class ViewTests(TestCase):
    def test_email_report_without_template(self):
        settings.REPORT_BUILDER_EMAIL_NOTIFICATION = True
        email_subject = getattr(settings, 'REPORT_BUILDER_EMAIL_SUBJECT', False) or "Report is ready"
        user = User.objects.get_or_create(username='example', email='to@example.com')[0]
        email_report(email_subject, user)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, email_subject)
        settings.REPORT_BUILDER_EMAIL_NOTIFICATION = None
        mail.outbox = []

    def test_email_report_with_template(self):
        settings.REPORT_BUILDER_EMAIL_NOTIFICATION = True
        report_url = 'http://fakeurl.com/fakestuffs'
        username = 'example'
        email_subject = getattr(settings, 'REPORT_BUILDER_EMAIL_SUBJECT', False) or "Report is ready"
        user = User.objects.get_or_create(username=username, email='to@example.com')[0]
        email_report(report_url, user)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, email_subject)
        self.assertEqual(mail.outbox[0].alternatives[0][0], "<p>Hello {0},</p>\n<br>\n<p>The report is <a href='{1}'>here</u></p>".format(username, report_url))
        settings.REPORT_BUILDER_EMAIL_NOTIFICATION = None
        settings.REPORT_BUILDER_EMAIL_TEMPLATE = None
        mail.outbox = []

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True)
    def test_report_builder_file_async_report_save(self):
        """
        Test to ensure the celery task will succeed given proper params in the right order.
        """
        user = User.objects.create(username='testy', is_staff=True, is_superuser=True)
        report = baker.make('Report')
        res = report_builder_file_async_report_save.delay(report.id, user.id, 'xlsx')
        self.assertEqual(res.successful(), True)
