from django import forms
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.db import models
from django.db.models import Avg, Min, Max, Count, Sum
from django.db.models.fields import FieldDoesNotExist
from report_builder.unique_slugify import unique_slugify
from report_utils.model_introspection import get_model_from_path_string
from dateutil import parser
from decimal import Decimal
import time
import datetime

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


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

    def _get_allowed_models():
        models = ContentType.objects.all()
        if getattr(settings, 'REPORT_BUILDER_INCLUDE', False):
            models = models.filter(name__in=settings.REPORT_BUILDER_INCLUDE)
        if getattr(settings, 'REPORT_BUILDER_EXCLUDE', False):
            models = models.exclude(name__in=settings.REPORT_BUILDER_EXCLUDE)
        return models

    name = models.CharField(max_length=255)
    slug = models.SlugField(verbose_name="Short Name")
    description = models.TextField(blank=True)
    root_model = models.ForeignKey(
        ContentType, limit_choices_to={'pk__in': _get_allowed_models})
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    user_created = models.ForeignKey(
        AUTH_USER_MODEL, editable=False, blank=True, null=True)
    user_modified = models.ForeignKey(
        AUTH_USER_MODEL, editable=False, blank=True, null=True,
        related_name="report_modified_set")
    distinct = models.BooleanField(default=False)
    report_file = models.FileField(upload_to="report_files", blank=True)
    report_file_creation = models.DateTimeField(blank=True, null=True)
    starred = models.ManyToManyField(
        AUTH_USER_MODEL, blank=True,
        help_text="These users have starred this report for easy reference.",
        related_name="report_starred_set")

    def save(self, *args, **kwargs):
        if not self.id:
            unique_slugify(self, self.name)
        super(Report, self).save(*args, **kwargs)

    def add_aggregates(self, queryset):
        for display_field in self.displayfield_set.filter(aggregate__isnull=False):
            if display_field.aggregate == "Avg":
                queryset = queryset.annotate(Avg(display_field.path + display_field.field))
            elif display_field.aggregate == "Max":
                queryset = queryset.annotate(Max(display_field.path + display_field.field))
            elif display_field.aggregate == "Min":
                queryset = queryset.annotate(Min(display_field.path + display_field.field))
            elif display_field.aggregate == "Count":
                queryset = queryset.annotate(Count(display_field.path + display_field.field))
            elif display_field.aggregate == "Sum":
                queryset = queryset.annotate(Sum(display_field.path + display_field.field))
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
            return model._meta.get_field_by_name(
                field_name)[0].get_internal_type()
        except FieldDoesNotExist:
            pass
        # Is it a property?
        field_attr = getattr(model, field_name, None)
        if isinstance(field_attr, property):
            return "Property"
        return model._meta.get_field_by_name(
            field_name)[0].get_internal_type()
        return "Invalid"

    def get_query(self):
        report = self
        model_class = self.root_model_class
        message= ""

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
        for filter_field in report.filterfield_set.all():
            # exclude properties from standard ORM filtering
            if filter_field.field_type == "Property":
                continue
            if filter_field.field_type == "Custom":
                continue

            filter_string = str(filter_field.path + filter_field.field)

            if filter_field.filter_type:
                filter_string += '__' + filter_field.filter_type

            # Check for special types such as isnull
            if (filter_field.filter_type == "isnull"
                    and filter_field.filter_value in ["0", "False"]):
                filter_ = {filter_string: False}
            elif filter_field.filter_type == "in":
                filter_ = {filter_string: filter_field.filter_value.split(',')}
            else:
                filter_value = filter_field.filter_value
                if filter_field.filter_type == 'range':
                    filter_value = [filter_value, filter_field.filter_value2]
                filter_ = {filter_string: filter_value}

            if not filter_field.exclude:
                filters.update(filter_)
            else:
                excludes.update(filter_)

        if filters:
            objects = objects.filter(**filters)
        if excludes:
            objects = objects.exclude(**excludes)

        # Aggregates
        objects = self.add_aggregates(objects)

        # Distinct
        if report.distinct:
            objects = objects.distinct()

        return objects, message

    @models.permalink
    def get_absolute_url(self):
        return ("report_update_view", [str(self.id)])

    def edit(self):
        return mark_safe('<a href="{0}"><img style="width: 26px; margin: -6px" src="{1}report_builder/img/edit.svg"/></a>'.format(
            self.get_absolute_url(),
            getattr(settings, 'STATIC_URL', '/static/')
        ))
    edit.allow_tags = True

    def download_xlsx(self):
        if getattr(settings, 'REPORT_BUILDER_ASYNC_REPORT', False):
            return mark_safe('<a href="javascript:void(0)" onclick="get_async_report({0})"><img style="width: 26px; margin: -6px" src="{1}report_builder/img/download.svg"/></a>'.format(
                self.id,
                getattr(settings, 'STATIC_URL', '/static/'),
            ))
        else:
            return mark_safe('<a href="{0}"><img style="width: 26px; margin: -6px" src="{1}report_builder/img/download.svg"/></a>'.format(
                reverse('report_download_xlsx', args=[self.id]),
                getattr(settings, 'STATIC_URL', '/static/'),
            ))
    download_xlsx.short_description = "Download"
    download_xlsx.allow_tags = True


    def copy_report(self):
        return '<a href="{0}"><img style="width: 26px; margin: -6px" src="{1}report_builder/img/copy.svg"/></a>'.format(
            reverse('report_builder.views.create_copy', args=[self.id]),
            getattr(settings, 'STATIC_URL', '/static/'),
        )
    copy_report.short_description = "Copy"
    copy_report.allow_tags = True

    def check_report_display_field_positions(self):
        """ After report is saved, make sure positions are sane
        """
        for i, display_field in enumerate(self.displayfield_set.all()):
            if display_field.position != i+1:
                display_field.position = i+1
                display_field.save()


class Format(models.Model):
    """ A specifies a Python string format for e.g. `DisplayField`s.
    """
    name = models.CharField(max_length=50, blank=True, default='')
    string = models.CharField(max_length=300, blank=True, default='', help_text='Python string format. Ex ${} would place a $ in front of the result.')

    def __unicode__(self):
        return self.name


class DisplayField(models.Model):
    """ A display field to show in a report. Always belongs to a Report
    """
    report = models.ForeignKey(Report)
    path = models.CharField(max_length=2000, blank=True)
    path_verbose = models.CharField(max_length=2000, blank=True)
    field = models.CharField(max_length=2000)
    field_verbose = models.CharField(max_length=2000)
    name = models.CharField(max_length=2000)
    sort = models.IntegerField(blank=True, null=True)
    sort_reverse = models.BooleanField(verbose_name="Reverse", default=False)
    width = models.IntegerField(default=15)
    aggregate = models.CharField(
        max_length=5,
        choices = (
            ('Sum','Sum'),
            ('Count','Count'),
            ('Avg','Avg'),
            ('Max','Max'),
            ('Min','Min'),
        ),
        blank = True
    )
    position = models.PositiveSmallIntegerField(blank = True, null = True)
    total = models.BooleanField(default=False)
    group = models.BooleanField(default=False)
    display_format = models.ForeignKey(Format, blank=True, null=True)

    class Meta:
        ordering = ['position']

    def get_choices(self, model, field_name):
        try:
            model_field = model._meta.get_field_by_name(field_name)[0]
        except:
            model_field = None
        if model_field and model_field.choices:
            # See https://github.com/burke-software/django-report-builder/pull/93
            return ((model_field.get_prep_value(key), val) for key, val in model_field.choices)

    @property
    def field_type(self):
        return self.report.get_field_type(self.field, self.path)

    @property
    def choices_dict(self):
        choices = self.choices
        choices_dict = {}
        if choices:
            for choice in choices:
                choices_dict.update({choice[0]: choice[1]})
        return choices_dict

    @property
    def choices(self):
        if self.pk:
            model = get_model_from_path_string(self.report.root_model.model_class(), self.path)
            return self.get_choices(model, self.field)

    def __unicode__(self):
        return self.name


class FilterField(models.Model):
    """ A display field to show in a report. Always belongs to a Report
    """
    report = models.ForeignKey(Report)
    path = models.CharField(max_length=2000, blank=True)
    path_verbose = models.CharField(max_length=2000, blank=True)
    field = models.CharField(max_length=2000)
    field_verbose = models.CharField(max_length=2000)
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
            ('week_day', 'Week day'),
            ('isnull', 'Is null'),
            ('regex', 'Regular Expression'),
            ('iregex', 'Reg. Exp. (case-insensitive)'),
        ),
        blank=True,
        default = 'icontains',
    )
    filter_value = models.CharField(max_length=2000)
    filter_value2 = models.CharField(max_length=2000, blank=True)
    exclude = models.BooleanField(default=False)
    position = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        ordering = ['position']

    def clean(self):
        if self.filter_type == "range":
            if self.filter_value2 in [None, ""]:
                raise ValidationError('Range filters must have two values')
        if self.field_type == "DateField":
            date_form = forms.DateField()
            date_value = parser.parse(self.filter_value).date()
            date_form.clean(date_value)
            self.filter_value = str(date_value)
        return super(FilterField, self).clean()

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
        if filter_type == 'isnull' and value == None:
            filtered = False
        if filter_type == 'regex' and re.search(filter_value, value):
            filtered = False
        if filter_type == 'iregex' and re.search(filter_value, value, re.I):
            filtered = False

        if filter_field.exclude:
            return not filtered
        return filtered

    @property
    def field_type(self):
        return self.report.get_field_type(self.field, self.path)

    @property
    def choices(self):
        if self.pk:
            model = get_model_from_path_string(
                self.report.root_model.model_class(), self.path)
            return self.get_choices(model, self.field)

    def __unicode__(self):
        return self.field
