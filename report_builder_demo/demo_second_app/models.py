from django.db import models


class Bar(models.Model):
    char_field = models.CharField(max_length=50, blank=True)

    @property
    def i_want_char_field(self):
        return 'lol no'

    class ReportBuilder:
        extra = ('i_want_char_field',)
