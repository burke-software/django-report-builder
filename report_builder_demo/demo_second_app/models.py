from django.db import models
from custom_field.custom_field import CustomFieldModel


class Bar(CustomFieldModel, models.Model):
    char_field = models.CharField(max_length=50, blank=True)

    @property
    def i_want_char_field(self):
        return 'lol no'

    class ReportBuilder:
        extra = ('i_want_char_field',)
