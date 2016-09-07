# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report_builder', '0005_report_chart_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='chart_style',
            field=models.CharField(max_length=16, null=True, blank=True),
        ),
    ]
