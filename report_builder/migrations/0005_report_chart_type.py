# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report_builder', '0004_auto_20160906_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='chart_type',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
