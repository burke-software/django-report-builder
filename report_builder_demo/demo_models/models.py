from django.db import models
from custom_field.custom_field import CustomFieldModel


class Foo(models.Model):
    char_field = models.CharField(max_length=50, blank=True)
    char_field2 = models.CharField(max_length=50, blank=True)

    class ReportBuilder:
        fields = ('char_field',)


class FooExclude(Foo):
    class ReportBuilder:
        exclude = ('char_field2',)


class Bar(CustomFieldModel, models.Model):
    char_field = models.CharField(max_length=50, blank=True)
    foos = models.ManyToManyField(Foo, blank=True)

    @property
    def i_want_char_field(self):
        return 'lol no'

    class ReportBuilder:
        extra = ('i_want_char_field',)
