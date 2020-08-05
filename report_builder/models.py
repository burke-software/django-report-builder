from django import forms
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError, ObjectDoesNotExist, FieldDoesNotExist
from django.utils.safestring import mark_safe
from django.utils.functional import cached_property
from django.db import models
from django.db.models import Avg, Min, Max, Count, Sum, F
from report_builder.unique_slugify import unique_slugify
from .utils import (
    get_model_from_path_string, sort_data, increment_total, formatter)
from .mixins import generate_filename, DataExportMixin
from .email import email_report
from dateutil import parser
from decimal import Decimal
from functools import reduce
import time
import datetime
import re

try:
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


def get_allowed_models():
    models = ContentType.objects.all()
    if getattr(settings, 'REPORT_BUILDER_INCLUDE', False):
        all_model_names = []
        additional_models = []
        for element in settings.REPORT_BUILDER_INCLUDE:
            split_element = element.split('.')
            if len(split_element) == 2:
                additional_models.append(models.filter(app_label=split_element[0], model=split_element[1]))
            else:
                all_model_names.append(element)
        models = models.filter(model__in=all_model_names)
        for additional_model in additional_models:
            models = models | additional_model
    if getattr(settings, 'REPORT_BUILDER_EXCLUDE', False):
        all_model_names = []
        for element in settings.REPORT_BUILDER_EXCLUDE:
            split_element = element.split('.')
            if len(split_element) == 2:
                models = models.exclude(app_label=split_element[0], model=split_element[1])
            else:
                all_model_names.append(element)
        models = models.exclude(model__in=all_model_names)
    return models


def get_limit_choices_to_callable():
    return {'pk__in': get_allowed_models()}


class Report(models.Model):
    """ A saved report with queryset and descriptive fields
    """
    def _get_model_manager(self):
        """ Get  manager from settings else use objects
        """
        model_manager = 'objects'
        if getattr(settings, 'REPORT_BUILDER_MODEL_MANAGER', False):
            model_manager = settings.REPORT_BUILDER_MODEL_MANAGER
        return model_manager

    @staticmethod
    def allowed_models():
        return get_allowed_models()

    name = models.CharField(max_length=255)
    slug = models.SlugField(verbose_name="Short Name")
    description = models.TextField(blank=True)
    root_model = models.ForeignKey(
        ContentType, limit_choices_to=get_limit_choices_to_callable,
        on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    user_created = models.ForeignKey(
        AUTH_USER_MODEL, editable=False, blank=True, null=True,
        on_delete=models.SET_NULL)
    user_modified = models.ForeignKey(
        AUTH_USER_MODEL, editable=False, blank=True, null=True,
        related_name="report_modified_set", on_delete=models.SET_NULL)
    distinct = models.BooleanField(default=False)
    report_file = models.FileField(upload_to="report_files", blank=True)
    report_file_creation = models.DateTimeField(blank=True, null=True)
    starred = models.ManyToManyField(
        AUTH_USER_MODEL, blank=True,
        help_text="These users have starred this report for easy reference.",
        related_name="report_starred_set")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            unique_slugify(self, self.name)
        super(Report, self).save(*args, **kwargs)

    def add_aggregates(self, queryset, display_fields=None):
        agg_funcs = {
            'Avg': Avg, 'Min': Min, 'Max': Max, 'Count': Count, 'Sum': Sum
        }
        if display_fields is None:
            display_fields = self.displayfield_set.filter(
                aggregate__isnull=False)
        for display_field in display_fields:
            if display_field.aggregate:
                func = agg_funcs[display_field.aggregate]
                full_name = display_field.path + display_field.field
                queryset = queryset.annotate(func(full_name))

        return queryset

    @property
    def root_model_class(self):
        return self.root_model.model_class()

    def get_field_type(self, field_name, path=""):
        """ Get field type for given field name.
        field_name is the full path of the field
        path is optional
        """
        model = get_model_from_path_string(
            self.root_model_class, path + field_name)

        # Is it a ORM field?
        try:
            return model._meta.get_field(field_name).get_internal_type()
        except FieldDoesNotExist:
            pass
        # Is it a property?
        field_attr = getattr(model, field_name, None)
        if isinstance(field_attr, (property, cached_property)):
            return "Property"
        # Is it a custom field?
        try:
            model().get_custom_field(field_name)
            return "Custom Field"
        except (ObjectDoesNotExist, AttributeError):
            pass
        return "Invalid"

    def get_good_display_fields(self):
        """ Returns only valid display fields """
        display_fields = self.displayfield_set.all()
        bad_display_fields = []
        for display_field in display_fields:
            if display_field.field_type == "Invalid":
                bad_display_fields.append(display_field)
        return display_fields.exclude(id__in=[o.id for o in bad_display_fields])

    def report_to_list(self, queryset=None, user=None, preview=False):
        """Convert report into list."""
        property_filters = []
        if queryset is None:
            queryset = self.get_query()
            for field in self.filterfield_set.all():
                if field.field_type in ["Property"]:
                    property_filters += [field]
        display_fields = self.get_good_display_fields()

        # Need the pk for inserting properties later
        display_field_paths = ['pk']
        display_field_properties = []
        display_totals = []
        insert_property_indexes = []
        choice_lists = {}
        display_formats = {}
        i = 0
        for display_field in display_fields:
            if display_field.total:
                display_field.total_count = Decimal(0.0)
                display_totals.append(display_field)
            display_field_type = display_field.field_type
            if display_field_type == "Property":
                display_field_properties.append(display_field.field_key)
                insert_property_indexes.append(i)
            else:
                if display_field.aggregate:
                    display_field_paths += [
                        display_field.field_key +
                        '__' + display_field.aggregate.lower()]
                else:
                    display_field_paths += [display_field.field_key]
            i += 1

            # Build display choices list
            if display_field.choices and hasattr(display_field, 'choices_dict'):
                choice_list = display_field.choices_dict
                # Insert blank and None as valid choices.
                choice_list[''] = ''
                choice_list[None] = ''
                choice_lists[display_field.position] = choice_list

            # Build display format list
            if (
                hasattr(display_field, 'display_format') and
                display_field.display_format
            ):
                display_formats[display_field.position] = \
                    display_field.display_format

        property_filters = []
        for filter_field in self.filterfield_set.all():
            filter_field_type = filter_field.field_type
            if filter_field_type == "Property":
                property_filters += [field]

        group = [df.path + df.field for df in display_fields if df.group]

        # To support group-by with multiple fields, we turn all the other
        # fields into aggregations. The default aggregation is `Max`.
        if group:
            for field in display_fields:
                if (not field.group) and (not field.aggregate):
                    field.aggregate = 'Max'
            values = queryset.values(*group)
            values = self.add_aggregates(values, display_fields)
            data_list = []
            for row in values:
                row_data = []
                for field in display_field_paths:
                    if field == 'pk':
                        continue
                    try:
                        row_data.append(row[field])
                    except KeyError:
                        row_data.append(row[field + '__max'])
                for total in display_totals:
                    increment_total(total, row_data)
                data_list.append(row_data)
        else:
            values_list = list(queryset.values_list(*display_field_paths))

            data_list = []
            values_index = 0
            for obj in queryset:
                display_property_values = []
                for display_property in display_field_properties:
                    relations = display_property.split('__')
                    val = reduce(getattr, relations, obj)
                    display_property_values.append(val)

                value_row = values_list[values_index]
                while value_row[0] == obj.pk:
                    add_row = True
                    data_row = list(value_row[1:])  # Remove added pk
                    # Insert in the location dictated by the order of display fields
                    for i, prop_value in enumerate(display_property_values):
                        data_row.insert(insert_property_indexes[i], prop_value)
                    for property_filter in property_filters:
                        relations = property_filter.field_key.split('__')
                        val = reduce(getattr, relations, obj)
                        if property_filter.filter_property(val):
                            add_row = False

                    if add_row is True:
                        for total in display_totals:
                            increment_total(total, data_row)
                        # Replace choice data with display choice string
                        for position, choice_list in choice_lists.items():
                            try:
                                data_row[position] = str(choice_list[data_row[position]])
                            except Exception:
                                data_row[position] = str(data_row[position])
                        for position, style in display_formats.items():
                            data_row[position] = formatter(data_row[position], style)
                        data_list.append(data_row)
                    values_index += 1
                    try:
                        value_row = values_list[values_index]
                    except IndexError:
                        break

        for display_field in display_fields.filter(
            sort__gt=0
        ).order_by('-sort'):
            data_list = sort_data(data_list, display_field)

        if display_totals:
            display_totals_row = []
            i = 0
            for display_field in display_totals:
                while i < display_field.position:
                    i += 1
                    display_totals_row.append('')
                i += 1
                display_totals_row.append(display_field.total_count)
            # Add formats to display totals
            for pos, style in display_formats.items():
                display_totals_row[pos] = formatter(display_totals_row[pos], style)

            data_list += [
                ['TOTALS'] + (len(display_fields) - 1) * ['']
            ] + [display_totals_row]

        return data_list

    def get_query(self):
        report = self
        model_class = self.root_model_class

        # Check for report_builder_model_manger property on the model
        if getattr(model_class, 'report_builder_model_manager', False):
            objects = getattr(model_class, 'report_builder_model_manager').all()
        else:
            # Get global model manager
            manager = report._get_model_manager()
            objects = getattr(model_class, manager).all()

        # Filters
        # NOTE: group all the filters together into one in order to avoid
        # unnecessary joins
        filters = {}
        excludes = {}
        for filter_field in report.filterfield_set.order_by('position'):
            # exclude properties from standard ORM filtering
            if filter_field.field_type == "Property":
                continue
            if filter_field.field_type == "Custom Field":
                continue
            if filter_field.filter_type in ('max', 'min'):
                # Annotation-filters are handled below.
                continue

            filter_string = str(filter_field.path + filter_field.field)

            if filter_field.filter_type:
                ft = filter_field.filter_type
                fs = ft if ft != 'relative_range' else 'range'
                filter_string += '__' + fs

            # Check for special types such as isnull
            if (filter_field.filter_type == "isnull" and
               filter_field.filter_value in ["0", "False"]):
                filter_ = {filter_string: False}
            elif filter_field.filter_type == "in":
                filter_ = {filter_string: filter_field.filter_value.split(',')}
            else:
                # Check for range and relative_range types
                filter_value = filter_field.filter_value
                if filter_field.filter_type == 'range':
                    filter_value = sorted([filter_value, filter_field.filter_value2])
                elif filter_field.filter_type == 'relative_range':
                    filter_value = filter_field.get_relative_range()
                filter_ = {filter_string: filter_value}

            if not filter_field.exclude:
                filters.update(filter_)
            else:
                excludes.update(filter_)

        if filters:
            objects = objects.filter(**filters)
        if excludes:
            objects = objects.exclude(**excludes)

        # Apply annotation-filters after regular filters.
        for filter_field in report.filterfield_set.order_by('position'):
            if filter_field.filter_type in ('max', 'min'):
                func = {'max': Max, 'min': Min}[filter_field.filter_type]
                column_name = '{0}{1}__{2}'.format(
                    filter_field.path,
                    filter_field.field,
                    filter_field.field_type
                )
                filter_string = filter_field.path + filter_field.field
                annotate_args = {column_name: func(filter_string)}
                filter_args = {column_name: F(filter_field.field)}
                objects = objects.annotate(**annotate_args).filter(**filter_args)

        # Aggregates
        objects = self.add_aggregates(objects)

        # Distinct
        if report.distinct:
            objects = objects.distinct()

        return objects

    def get_absolute_url(self):
        return reverse("report_update_view", args=(self.id,))

    def edit(self):
        return mark_safe(
            '<a href="{0}"><img style="width: 26px; margin: -6px" src="{1}report_builder/img/edit.svg"/></a>'.format(
                self.get_absolute_url(),
                getattr(settings, 'STATIC_URL', '/static/')
            )
        )
    edit.allow_tags = True

    def download_xlsx(self):
        if getattr(settings, 'REPORT_BUILDER_ASYNC_REPORT', False):
            return mark_safe(
                '<a href="javascript:void(0)" onclick="get_async_report({0})"><img style="width: 26px; margin: -6px" src="{1}report_builder/img/download.svg"/></a>'.format(
                    self.id,
                    getattr(settings, 'STATIC_URL', '/static/'),
                )
            )
        else:
            return mark_safe(
                '<a href="{0}"><img style="width: 26px; margin: -6px" src="{1}report_builder/img/download.svg"/></a>'.format(
                    reverse('report_download_file', args=[self.id]),
                    getattr(settings, 'STATIC_URL', '/static/'),
                )
            )
    download_xlsx.short_description = "Download"
    download_xlsx.allow_tags = True

    def copy_report(self):
        return mark_safe('<a href="{0}"><img style="width: 26px; margin: -6px" src="{1}report_builder/img/copy.svg"/></a>'.format(
            reverse('report_builder_create_copy', args=[self.id]),
            getattr(settings, 'STATIC_URL', '/static/'),
        ))
    copy_report.short_description = "Copy"
    copy_report.allow_tags = True

    def check_report_display_field_positions(self):
        """ After report is saved, make sure positions are sane
        """
        for i, display_field in enumerate(self.displayfield_set.all()):
            if display_field.position != i + 1:
                display_field.position = i + 1
                display_field.save()

    def email_report(self, user=None, email=None):
        report_url = self.report_file.url
        return email_report(report_url, user=user, email=email)

    def async_report_save(self, objects_list,
                          title, header, widths, user=None, file_type="xlsx", email_to:str = None):
        data_export = DataExportMixin()
        if file_type == 'csv':
            csv_file = data_export.list_to_csv_file(objects_list, title,
                                                    header, widths)
            title = generate_filename(title, '.csv')
            self.report_file.save(title, ContentFile(csv_file.getvalue().encode()))
        else:
            xlsx_file = data_export.list_to_xlsx_file(objects_list, title,
                                                      header, widths)
            title = generate_filename(title, '.xlsx')
            self.report_file.save(title, ContentFile(xlsx_file.getvalue()))
        self.report_file_creation = datetime.datetime.today()
        self.save()
        if email_to:
            for email in email_to:
                self.email_report(email=email)
        elif getattr(settings, 'REPORT_BUILDER_EMAIL_NOTIFICATION', False):
            if user.email:
                self.email_report(user=user)

    def run_report(self, file_type, user=None, queryset=None, asynchronous=False, scheduled=False, email_to:str = None):
        """Generate this report file"""
        if not queryset:
            queryset = self.get_query()

        display_fields = self.get_good_display_fields()

        data_export = DataExportMixin()
        objects_list, message = data_export.report_to_list(
            queryset, display_fields, user, preview=False)
        title = re.sub(r'\W+', '', self.name)[:30]
        header = []
        widths = []
        for field in display_fields:
            header.append(field.name)
            widths.append(field.width)
        if scheduled:
            self.async_report_save(objects_list, title, header, widths, file_type, email_to=email_to)
        elif asynchronous:
            if user is None:
                raise Exception('Cannot run async report without a user')
            self.async_report_save(objects_list, title, header, widths, user, file_type)
        else:
            if file_type == 'csv':
                return data_export.list_to_csv_response(
                    objects_list, title, header, widths)
            else:
                return data_export.list_to_xlsx_response(
                    objects_list, title, header, widths)


class Format(models.Model):
    """ A specifies a Python string format for e.g. `DisplayField`s.
    """
    name = models.CharField(max_length=50, blank=True, default='')
    string = models.CharField(
        max_length=300, blank=True, default='',
        help_text='Python string format. Ex ${} would place a $ in front of the result.'
    )

    def __str__(self):
        return self.name


class AbstractField(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    path = models.CharField(max_length=2000, blank=True)
    path_verbose = models.CharField(max_length=2000, blank=True)
    field = models.CharField(max_length=2000)
    field_verbose = models.CharField(max_length=2000)
    position = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ['position']

    @property
    def field_type(self):
        return self.report.get_field_type(self.field, self.path)

    @property
    def field_key(self):
        """ This key can be passed to a Django ORM values_list """
        return self.path + self.field

    @property
    def choices(self):
        if self.pk:
            model = get_model_from_path_string(
                self.report.root_model.model_class(), self.path)
            return self.get_choices(model, self.field)


class DisplayField(AbstractField):
    """ A display field to show in a report. Always belongs to a Report
    """
    name = models.CharField(max_length=2000)
    sort = models.IntegerField(blank=True, null=True)
    sort_reverse = models.BooleanField(verbose_name="Reverse", default=False)
    width = models.IntegerField(default=15)
    aggregate = models.CharField(
        max_length=5,
        choices=(
            ('Sum', 'Sum'),
            ('Count', 'Count'),
            ('Avg', 'Avg'),
            ('Max', 'Max'),
            ('Min', 'Min'),
        ),
        blank=True
    )
    total = models.BooleanField(default=False)
    group = models.BooleanField(default=False)
    display_format = models.ForeignKey(Format, blank=True, null=True,
        on_delete=models.SET_NULL)

    def get_choices(self, model, field_name):
        try:
            model_field = model._meta.get_field_by_name(field_name)[0]
        except:
            model_field = None
        if model_field and model_field.choices:
            return ((model_field.get_prep_value(key), val) for key, val in model_field.choices)

    @property
    def choices_dict(self):
        choices = self.choices
        choices_dict = {}
        if choices:
            for choice in choices:
                choices_dict.update({choice[0]: choice[1]})
        return choices_dict

    def __str__(self):
        return self.name


class FilterField(AbstractField):
    """
    A filter model used to filter DisplayFields using Django ORM
    filter arguments or custom filter values.
    """

    filter_type = models.CharField(
        max_length=20,
        choices=(
            ('exact', 'Equals'),
            ('iexact', 'Equals (case-insensitive)'),
            ('contains', 'Contains'),
            ('icontains', 'Contains (case-insensitive)'),
            ('in', 'in (comma seperated 1,2,3)'),
            ('gt', 'Greater than'),
            ('gte', 'Greater than equals'),
            ('lt', 'Less than'),
            ('lte', 'Less than equals'),
            ('startswith', 'Starts with'),
            ('istartswith', 'Starts with (case-insensitive)'),
            ('endswith', 'Ends with'),
            ('iendswith', 'Ends with  (case-insensitive)'),
            ('range', 'range'),
            ('relative_range', 'relative_range'),
            ('week_day', 'Week day'),
            ('isnull', 'Is null'),
            ('regex', 'Regular Expression'),
            ('iregex', 'Reg. Exp. (case-insensitive)'),
            ('max', 'Max (annotation-filter)'),
            ('min', 'Min (annotation-filter)'),
        ),
        blank=True,
        default='icontains',
    )
    filter_delta = models.BigIntegerField(null=True, blank=True)
    filter_value = models.CharField(max_length=2000, blank=True)
    filter_value2 = models.CharField(max_length=2000, blank=True)
    exclude = models.BooleanField(default=False)

    def clean(self):
        dt_types = ['DateField', 'DateTimeField', 'TimeField']

        if self.filter_type == 'range' and self.filter_value2 in [None, '']:
            raise ValidationError('Range filters must have two values')

        # Raise error if 'relative_range' filter is applied to a non-supported
        # field type
        if self.filter_type == 'relative_range' and self.field_type not in dt_types:
            raise ValidationError(
                'Relative Range filtering is only currently supported for'
                ' the following field types: {}.'.format(dt_types))

        # Check for required relative range filter_delta
        if self.filter_type == 'relative_range' and self.filter_delta is None:
            raise ValidationError(
                'Relative Range filters must have value and delta inputs.')

        if self.filter_type in ('max', 'min'):
            # These filter types ignore their value.
            pass

        # clean DateTimeField inputs
        elif self.field_type == 'DateField' and self.filter_type != 'isnull':
            self.filter_value = str(self.parse_datetime_fields(self.filter_value))

        return super(FilterField, self).clean()

    def parse_datetime_fields(self, dt_type):
        """Clean and parse datetime filter_value inputs."""
        date_value = parser.parse(dt_type)
        date_form = forms.DateTimeField()

        if self.field_type == 'DateField':
            date_value = date_value.date()
            date_form = forms.DateField()
        if self.field_type == 'TimeField':
            date_value = date_value.time()
            date_form = forms.TimeField()

        return date_form.clean(date_value)

    def get_choices(self, model, field_name):
        try:
            model_field = model._meta.get_field_by_name(field_name)[0]
        except:
            model_field = None
        if model_field and model_field.choices:
            return model_field.choices

    def filter_property(self, value):
        """ Determine if passed value should be filtered or not """
        filter_field = self
        filter_type = filter_field.filter_type
        filter_value = filter_field.filter_value
        filtered = True
        WEEKDAY_INTS = {
            'monday': 0,
            'tuesday': 1,
            'wednesday': 2,
            'thursday': 3,
            'friday': 4,
            'saturday': 5,
            'sunday': 6,
        }
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
        if filter_type == 'isnull' and value is None:
            filtered = False
        if filter_type == 'regex' and re.search(filter_value, value):
            filtered = False
        if filter_type == 'iregex' and re.search(filter_value, value, re.I):
            filtered = False

        if filter_field.exclude:
            return not filtered
        return filtered

    def get_relative_range(self):
        """
        Generate a 'filterable' range from the current date and filter delta.
        Ex.
            With:
                self.filter_type = 'relative_range'
                self.filter_delta = -60 * 60 * 24 * 2 (i.e. -2 days)
            Return:
                # a 'negative' two day range from filter_value
                ["2017-01-01", "2017-01-03"]
        """
        day = 60 * 60 * 24

        if self.field_type == 'DateField':
            if abs(self.filter_delta) < day:
                raise ValidationError(
                    'DateField delta must be at least 1 day.')
            first = datetime.date.today()
            second = first + datetime.timedelta(seconds=self.filter_delta)
            output_range = sorted([first, second])
            output = [date.strftime("%Y-%m-%d") for date in output_range]

        elif self.field_type == 'DateTimeField':
            first = datetime.datetime.now()
            second = first + datetime.timedelta(seconds=self.filter_delta)
            output_range = sorted([first, second])
            output = [date.strftime("%Y-%m-%d %H:%M:%S") for date in output_range]

        elif self.field_type == 'TimeField':
            day_const = datetime.datetime(1, 1, 1)
            first = datetime.datetime.now().time()
            delta = datetime.timedelta(seconds=self.filter_delta)
            diff = datetime.datetime.combine(day_const, first) + delta
            second = diff.time()
            output_range = sorted([first, second])
            output = [date.strftime("%H:%M") for date in output_range]

        return output

    @property
    def field_type(self):
        return self.report.get_field_type(self.field, self.path)

    @property
    def choices(self):
        if self.pk:
            model = get_model_from_path_string(
                self.report.root_model.model_class(), self.path)
            return self.get_choices(model, self.field)

    def __str__(self):
        return self.field
