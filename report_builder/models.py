from django.contrib.contenttypes.models import ContentType
from django.db import models

class Report(models.Model):
    """ A saved report with queryset and descriptive fields
    """
    name = models.CharField(max_length=255)
    root_model = models.ForeignKey(ContentType)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    
    @models.permalink
    def get_absolute_url(self):
        return ("report_update_view", [str(self.id)])
    
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
    width = models.IntegerField(default=120)
    aggregate = models.CharField(
        max_length=5,
        choices = (
            ('Count','Sum'),
            ('Ave','Ave'),
            ('Max','Max'),
            ('Min','Min'),
        ),
        blank = True
    )
    position = models.PositiveSmallIntegerField(blank = True, null = True)
    class Meta:
        ordering = ['position']
    