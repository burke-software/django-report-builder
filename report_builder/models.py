from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.db import models
from django.db.models import Avg, Min, Max, Count, Sum
from django.db.models.signals import post_save
from report_builder.unique_slugify import unique_slugify
from dateutil import parser

class Report(models.Model):
    """ A saved report with queryset and descriptive fields
    """
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
    root_model = models.ForeignKey(ContentType, limit_choices_to={'pk__in':_get_allowed_models})
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    user_created = models.ForeignKey(User, editable=False, blank=True, null=True)
    user_modified = models.ForeignKey(User, editable=False, blank=True, null=True, related_name="report_modified_set")
    distinct = models.BooleanField()
    starred = models.ManyToManyField(User, blank=True,
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

    
    def get_query(self):
        report = self
        model_class = report.root_model.model_class()
        message= ""
        objects = model_class.objects.all()

        # Filters
        # NOTE: group all the filters together into one in order to avoid 
        # unnecessary joins
        filters = {}
        excludes = {}
        for filter_field in report.filterfield_set.all():
            try:
                # exclude properties from standard ORM filtering 
                if '[property]' in filter_field.field_verbose:
                    continue
                if '[custom' in filter_field.field_verbose:
                    continue

                filter_string = str(filter_field.path + filter_field.field)
                
                if filter_field.filter_type:
                    filter_string += '__' + filter_field.filter_type
                
                # Check for special types such as isnull
                if filter_field.filter_type == "isnull" and filter_field.filter_value == "0":
                    filter_ = {filter_string: False}
                else:
                    # All filter values are stored as strings, but may need to be converted
                    if '[Date' in filter_field.field_verbose:
                        filter_value = parser.parse(filter_field.filter_value)
                        if settings.USE_TZ:
                            filter_value = timezone.make_aware(
                                filter_value,
                                timezone.get_current_timezone()
                            )
                    else:
                        filter_value = filter_field.filter_value
                    filter_ = {filter_string: filter_value}

                if not filter_field.exclude:
                    filters.update(filter_) 
                else:
                    excludes.update(filter_) 

            except Exception, e:
                message += "Filter Error on %s. If you are using the report builder then " % filter_field.field_verbose
                message += "you found a bug! "
                message += "If you made this in admin, then you probably did something wrong."

        if filters:
            objects = objects.filter(**filters)
        if excludes:
            objects = objects.exclude(**excludes)

        # Aggregates
        objects = self.add_aggregates(objects) 

        # Distinct
        if report.distinct:
            objects = objects.distinct()

        return objects
    
    @models.permalink
    def get_absolute_url(self):
        return ("report_update_view", [str(self.id)])
    
    def edit(self):
        return mark_safe('<a href="%s"><img style="width: 26px; margin: -6px" src="/static/report_builder/img/edit.png"/></a>' % self.get_absolute_url())
    edit.allow_tags = True
    
    def download_xlsx(self):
        return mark_safe('<a href="{0}"><img style="width: 26px; margin: -6px" src="/static/report_builder/img/download.svg"/></a>'.format(
            reverse('report_builder.views.download_xlsx', args=[self.id])))
    download_xlsx.short_description = "Download"
    download_xlsx.allow_tags = True
    

    def copy_report(self):
        return '<a href="{0}"><img style="width: 26px; margin: -6px" src="/static/report_builder/img/copy.svg"/></a>'.format(
            reverse('report_builder.views.create_copy', args=[self.id]))
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
    sort_reverse = models.BooleanField(verbose_name="Reverse")
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
    
    def get_choices(self, path, field_name):
        model_name = path.split(':')[-1]
        model = ContentType.objects.get(model=model_name).model_class()
        try:
            model_field = model._meta.get_field_by_name(field_name)[0]
        except:
            model_field = None
        if model_field and model_field.choices:
            return model_field.choices

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
            path = self.path_verbose or self.report.root_model.model
            return self.get_choices(path, self.field)

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
        choices = (
            ('exact','Equals'),
            ('iexact','Equals (case-insensitive)'),
            ('contains','Contains'),
            ('icontains','Contains (case-insensitive)'),
            ('in','in (must be array like [1,2,3])'),
            ('gt','Greater than'),
            ('gte','Greater than equals'),
            ('lt','Less than'),
            ('lte','Less than equals'),
            ('startswith','Starts with'),
            ('istartswith','Starts with (case-insensitive)'),
            ('endswith','Ends with'),
            ('iendswith','Ends with  (case-insensitive)'),
            ('range','range'),
            ('week_day','Week day'),
            ('isnull','Is null'),
            ('regex','Regular Expression'),
            ('iregex','Regular Expression (case-insensitive)'),
        ),
        blank=True,
        default = 'icontains',
    )
    filter_value = models.CharField(max_length=2000)
    filter_value2 = models.CharField(max_length=2000, blank=True)
    exclude = models.BooleanField()
    position = models.PositiveSmallIntegerField(blank = True, null = True)

    class Meta:
        ordering = ['position']

    def get_choices(self, path, field_name):
        model_name = path.split(':')[-1]
        model = ContentType.objects.get(model=model_name).model_class()
        try:
            model_field = model._meta.get_field_by_name(field_name)[0]
        except:
            model_field = None
        if model_field and model_field.choices:
            return model_field.choices

    @property
    def choices(self):
        if self.pk:
            path = self.path_verbose or self.report.root_model.model
            return self.get_choices(path, self.field)

    def __unicode__(self):
        return self.field
    
