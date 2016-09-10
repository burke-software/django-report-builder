# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report_builder', '0009_auto_20160910_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='chart_series',
            field=models.CommaSeparatedIntegerField(max_length=64, null=True, blank=True),
        ),
    ]
