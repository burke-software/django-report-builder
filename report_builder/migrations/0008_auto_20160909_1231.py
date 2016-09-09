# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report_builder', '0007_auto_20160909_0916'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='chart_labels',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='report',
            name='chart_stacked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='report',
            name='chart_total',
            field=models.BooleanField(default=False),
        ),
    ]
