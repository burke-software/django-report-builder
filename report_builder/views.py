import datetime
import re
import copy
import json
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.files.base import ContentFile
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View
from six import string_types
from .utils import duplicate
from .models import Report
from report_utils.mixins import DataExportMixin, generate_filename

User = get_user_model()


class ReportSPAView(TemplateView):

    template_name = "report_builder/spa.html"

    def get_context_data(self, **kwargs):
        context = super(ReportSPAView, self).get_context_data(**kwargs)
        context['ASYNC_REPORT'] = getattr(
            settings, 'REPORT_BUILDER_ASYNC_REPORT', False
        )
        return context


def fieldset_string_to_field(fieldset_dict, model):
    if isinstance(fieldset_dict['fields'], tuple):
        fieldset_dict['fields'] = list(fieldset_dict['fields'])
    i = 0
    for dict_field in fieldset_dict['fields']:
        if isinstance(dict_field, string_types):
            fieldset_dict['fields'][i] = model._meta.get_field_by_name(
                dict_field)[0]
        elif isinstance(dict_field, list) or isinstance(dict_field, tuple):
            dict_field[1]['recursive'] = True
            fieldset_string_to_field(dict_field[1], model)
        i += 1


def get_fieldsets(model):
    """ fieldsets are optional, they are defined in the Model.
    """
    fieldsets = getattr(model, 'report_builder_fieldsets', None)
    if fieldsets:
        for fieldset_name, fieldset_dict in model.report_builder_fieldsets:
            fieldset_string_to_field(fieldset_dict, model)
    return fieldsets


def email_report(report_url, user):
    if ((getattr(settings, 'EMAIL_BACKEND', False) or
            getattr(settings, 'EMAIL_HOST', False)) and
            getattr(settings, 'DEFAULT_FROM_EMAIL', False)):
        if get_template('email/email_report.html'):
            email_template = get_template('email/email_report.html')
            msg = EmailMultiAlternatives(
                getattr(settings, 'REPORT_BUILDER_EMAIL_SUBJECT', False) or
                'Report is ready',
                report_url,
                getattr(settings, 'DEFAULT_FROM_EMAIL'),
                [user.email],
            )
            htmlParameters = {
                'name': user.first_name or user.username,
                'report': report_url,
            }
            msg.attach_alternative(
                email_template.render(Context(htmlParameters)),
                "text/html"
            )
            msg.send()
        else:
            send_mail(
                getattr(settings, 'REPORT_BUILDER_EMAIL_SUBJECT', False) or
                'Report is ready',
                str(report_url),
                getattr(settings, 'DEFAULT_FROM_EMAIL'),
                [user.email],
                fail_silently=True,
            )


class DownloadFileView(DataExportMixin, View):

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(DownloadFileView, self).dispatch(*args, **kwargs)

    def process_report(self, report_id, user_id,
                       file_type, to_response, queryset=None):
        report = get_object_or_404(Report, pk=report_id)
        user = User.objects.get(pk=user_id)
        if not queryset:
            queryset = report.get_query()

        display_fields = report.get_good_display_fields()

        objects_list, message = self.report_to_list(
            queryset,
            display_fields,
            user,
            preview=False,)
        title = re.sub(r'\W+', '', report.name)[:30]
        header = []
        widths = []
        for field in display_fields:
            header.append(field.name)
            widths.append(field.width)

        if to_response:
            if file_type == 'csv':
                return self.list_to_csv_response(
                    objects_list, title, header, widths)
            else:
                return self.list_to_xlsx_response(
                    objects_list, title, header, widths)
        else:
            self.async_report_save(report, objects_list,
                                   title, header, widths, user, file_type)

    def async_report_save(self, report, objects_list,
                          title, header, widths, user, file_type):
        if file_type == 'csv':
            csv_file = self.list_to_csv_file(objects_list, title,
                                             header, widths)
            title = generate_filename(title, '.csv')
            report.report_file.save(title, ContentFile(csv_file.getvalue()))
        else:
            xlsx_file = self.list_to_xlsx_file(objects_list, title,
                                               header, widths)
            title = generate_filename(title, '.xlsx')
            report.report_file.save(title, ContentFile(xlsx_file.getvalue()))
        report.report_file_creation = datetime.datetime.today()
        report.save()
        if getattr(settings, 'REPORT_BUILDER_EMAIL_NOTIFICATION', False):
            if user.email:
                email_report(report.report_file.url, user)

    def get(self, request, *args, **kwargs):
        report_id = kwargs['pk']
        file_type = kwargs.get('filetype')
        if getattr(settings, 'REPORT_BUILDER_ASYNC_REPORT', False):
            from .tasks import report_builder_file_async_report_save
            report_task = report_builder_file_async_report_save.delay(
                report_id, request.user.pk, file_type)
            task_id = report_task.task_id
            return HttpResponse(
                json.dumps({'task_id': task_id}),
                content_type="application/json")
        else:
            return self.process_report(
                report_id, request.user.pk, file_type, to_response=True)


@staff_member_required
def ajax_add_star(request, pk):
    """ Star or unstar report for user
    """
    report = get_object_or_404(Report, pk=pk)
    user = request.user
    if user in report.starred.all():
        added = False
        report.starred.remove(request.user)
    else:
        added = True
        report.starred.add(request.user)
    return HttpResponse(added)


@staff_member_required
def create_copy(request, pk):
    """ Copy a report including related fields """
    report = get_object_or_404(Report, pk=pk)
    new_report = duplicate(report, changes=(
        ('name', '{0} (copy)'.format(report.name)),
        ('user_created', request.user),
        ('user_modified', request.user),
    ))
    # duplicate does not get related
    for display in report.displayfield_set.all():
        new_display = copy.copy(display)
        new_display.pk = None
        new_display.report = new_report
        new_display.save()
    for report_filter in report.filterfield_set.all():
        new_filter = copy.copy(report_filter)
        new_filter.pk = None
        new_filter.report = new_report
        new_filter.save()
    return redirect(new_report)


class ExportToReport(DownloadFileView, TemplateView):
    """ Export objects (by ID and content type) to an existing or new report
    In effect this runs the report with it's display fields. It ignores
    filters and filters instead the provided ID's. It can be select
    as a global admin action.
    """
    template_name = "report_builder/export_to_report.html"

    def get_context_data(self, **kwargs):
        ctx = super(ExportToReport, self).get_context_data(**kwargs)
        ctx['admin_url'] = self.request.GET.get('admin_url', '/')
        ct = ContentType.objects.get_for_id(self.request.GET['ct'])
        ids = self.request.GET['ids'].split(',')
        ctx['ids'] = ",".join(map(str, ids))
        ctx['ct'] = ct.id
        ctx['number_objects'] = len(ids)
        ctx['object_list'] = Report.objects.filter(
            root_model=ct).order_by('-modified')
        ctx['mode'] = ct.model_class()._meta.verbose_name
        return ctx

    def get(self, request, *args, **kwargs):
        if 'download' in request.GET:
            ct = ContentType.objects.get_for_id(request.GET['ct'])
            ids = self.request.GET['ids'].split(',')
            report = get_object_or_404(Report, pk=request.GET['download'])
            queryset = ct.model_class().objects.filter(pk__in=ids)
            return self.process_report(
                report.id, request.user.pk,
                to_response=True,
                queryset=queryset,
                file_type="xlsx",
            )
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


@staff_member_required
def check_status(request, pk, task_id):
    """ Check if the asyncronous report is ready to download """
    from celery.result import AsyncResult
    res = AsyncResult(task_id)
    link = ''
    if res.state == 'SUCCESS':
        report = get_object_or_404(Report, pk=pk)
        link = report.report_file.url
    return HttpResponse(
        json.dumps({
            'state': res.state,
            'link': link,
            'email': getattr(
                settings,
                'REPORT_BUILDER_EMAIL_NOTIFICATION',
                False
            )
        }),
        content_type="application/json")
