# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('report_builder', '0002_auto_20150201_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='external_report_url',
            field=models.TextField(blank=True, null=True, validators=[django.core.validators.URLValidator()]),
        ),
    ]
