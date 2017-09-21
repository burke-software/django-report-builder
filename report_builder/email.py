from django.conf import settings
from django.template.loader import get_template
from django.core.mail import send_mail, EmailMultiAlternatives


def email_report(report_url, user=None, email=None):
    if ((getattr(settings, 'EMAIL_BACKEND', False) or
             getattr(settings, 'EMAIL_HOST', False)) and
            getattr(settings, 'DEFAULT_FROM_EMAIL', False)):

        name = None
        if user:
            email = user.email
            name = user.username

        if get_template('email/email_report.html'):
            email_template = get_template('email/email_report.html')
            msg = EmailMultiAlternatives(
                getattr(settings, 'REPORT_BUILDER_EMAIL_SUBJECT', False) or
                'Report is ready',
                report_url,
                getattr(settings, 'DEFAULT_FROM_EMAIL'),
                [email],
            )
            htmlParameters = {
                'name': name,
                'report': report_url,
            }
            msg.attach_alternative(
                email_template.render(htmlParameters),
                "text/html"
            )
            msg.send()
        else:
            send_mail(
                getattr(settings, 'REPORT_BUILDER_EMAIL_SUBJECT', False) or
                'Report is ready',
                str(report_url),
                getattr(settings, 'DEFAULT_FROM_EMAIL'),
                [email],
                fail_silently=True,
            )
