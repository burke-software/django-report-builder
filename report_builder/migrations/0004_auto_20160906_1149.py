# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report_builder', '0003_auto_20150720_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='chart_categories',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='report',
            name='chart_series',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='report',
            name='chart_values',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
