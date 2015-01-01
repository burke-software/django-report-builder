from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.files.base import ContentFile
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
User = get_user_model()
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View

from .utils import duplicate
from .models import Report
from report_utils.mixins import DataExportMixin

import datetime
import time
import re
from decimal import Decimal
import copy
from dateutil import parser
import json


class ReportSPAView(TemplateView):
    template_name = "report_builder/spa.html"

    def get_context_data(self, **kwargs):
        context = super(ReportSPAView, self).get_context_data(**kwargs)
        context['ASYNC_REPORT'] = settings.REPORT_BUILDER_ASYNC_REPORT
        return context

def filter_property(filter_field, value):
    filter_type = filter_field.filter_type
    filter_value = filter_field.filter_value
    filtered = True
    #TODO: i10n
    WEEKDAY_INTS = {
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'saturday': 5,
        'sunday': 6,
    }
    #TODO instead of catch all, deal with all cases
    # Example is 'a' < 2 is a valid python comparison
    # But what about 2 < '1' which yeilds true! Not intuitive for humans.
    try:
        if filter_type == 'exact' and str(value) == filter_value:
            filtered = False
        if filter_type == 'iexact' and str(value).lower() == str(filter_value).lower():
            filtered = False
        if filter_type == 'contains' and filter_value in value:
            filtered = False
        if filter_type == 'icontains' and str(filter_value).lower() in str(value).lower():
            filtered = False
        if filter_type == 'in' and value in filter_value:
            filtered = False
        # convert dates and datetimes to timestamps in order to compare digits and date/times the same
        if isinstance(value, datetime.datetime) or isinstance(value, datetime.date):
            value = str(time.mktime(value.timetuple()))
            try:
                filter_value_dt = parser.parse(filter_value)
                filter_value = str(time.mktime(filter_value_dt.timetuple()))
            except ValueError:
                pass
        if filter_type == 'gt' and Decimal(value) > Decimal(filter_value):
            filtered = False
        if filter_type == 'gte' and Decimal(value) >= Decimal(filter_value):
            filtered = False
        if filter_type == 'lt' and Decimal(value) < Decimal(filter_value):
            filtered = False
        if filter_type == 'lte' and Decimal(value) <= Decimal(filter_value):
            filtered = False
        if filter_type == 'startswith' and str(value).startswith(str(filter_value)):
            filtered = False
        if filter_type == 'istartswith' and str(value).lower().startswith(str(filter_value)):
            filtered = False
        if filter_type == 'endswith' and str(value).endswith(str(filter_value)):
            filtered = False
        if filter_type == 'iendswith' and str(value).lower().endswith(str(filter_value)):
            filtered = False
        if filter_type == 'range' and value in [int(x) for x in filter_value]:
            filtered = False
        if filter_type == 'week_day' and WEEKDAY_INTS.get(str(filter_value).lower()) == value.weekday:
            filtered = False
        if filter_type == 'isnull' and value == None:
            filtered = False
        if filter_type == 'regex' and re.search(filter_value, value):
            filtered = False
        if filter_type == 'iregex' and re.search(filter_value, value, re.I):
            filtered = False
    except:
        pass

    if filter_field.exclude:
        return not filtered
    return filtered


def fieldset_string_to_field(fieldset_dict, model):
    if isinstance(fieldset_dict['fields'], tuple):
        fieldset_dict['fields'] = list(fieldset_dict['fields'])
    i = 0
    for dict_field in fieldset_dict['fields']:
        if isinstance(dict_field, basestring):
            fieldset_dict['fields'][i] = model._meta.get_field_by_name(dict_field)[0]
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


class DownloadXlsxView(DataExportMixin, View):
    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(DownloadXlsxView, self).dispatch(*args, **kwargs)

    def process_report(self, report_id, user_id, to_response, queryset=None):
        report = get_object_or_404(Report, pk=report_id)
        user = User.objects.get(pk=user_id)
        if not queryset:
            queryset, message = report.get_query()
        property_filters = report.filterfield_set.filter(
            Q(field_verbose__contains='[property]') | Q(field_verbose__contains='[custom')
        )
        objects_list, message = self.report_to_list(
            queryset,
            report.displayfield_set.all(),
            user,
            property_filters=property_filters,
            preview=False,)
        title = re.sub(r'\W+', '', report.name)[:30]
        header = []
        widths = []
        for field in report.displayfield_set.all():
            header.append(field.name)
            widths.append(field.width)

        if to_response:
            return self.list_to_xlsx_response(objects_list, title, header, widths)
        else:
            self.async_report_save(report, objects_list, title, header, widths)

    def async_report_save(self, report, objects_list, title, header, widths):
        xlsx_file = self.list_to_xlsx_file(objects_list, title, header, widths)
        if not title.endswith('.xlsx'):
            title += '.xlsx'
        report.report_file.save(title, ContentFile(xlsx_file.getvalue()))
        report.report_file_creation = datetime.datetime.today()
        report.save()

    def get(self, request, *args, **kwargs):
        report_id = kwargs['pk']
        if getattr(settings, 'REPORT_BUILDER_ASYNC_REPORT', False):
            from .tasks import report_builder_async_report_save
            report_task = report_builder_async_report_save.delay(report_id, request.user.pk)
            task_id = report_task.task_id
            return HttpResponse(json.dumps({'task_id': task_id}), content_type="application/json")
        else:
            return self.process_report(report_id, request.user.pk, to_response=True)


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


class ExportToReport(DownloadXlsxView, TemplateView):
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
        ctx['object_list'] = Report.objects.filter(root_model=ct).order_by('-modified')
        ctx['mode'] = ct.model_class()._meta.verbose_name
        return ctx

    def get(self, request, *args, **kwargs):
        if 'download' in request.GET:
            ct = ContentType.objects.get_for_id(request.GET['ct'])
            ids = self.request.GET['ids'].split(',')
            report = get_object_or_404(Report, pk=request.GET['download'])
            queryset = ct.model_class().objects.filter(pk__in=ids)
            return self.process_report(
                report.id, request.user.pk, to_response=True, queryset=queryset)
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
    return HttpResponse(json.dumps({'state': res.state, 'link': link }), content_type="application/json")

