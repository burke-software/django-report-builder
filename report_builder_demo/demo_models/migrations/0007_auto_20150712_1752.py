# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demo_models', '0006_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bar',
            name='date_field',
        ),
        migrations.AlterField(
            model_name='bar',
            name='check_mate_status',
            field=models.CharField(max_length=2, default='CH', choices=[('CH', 'CHECK'), ('MA', 'CHECKMATE')]),
        ),
        migrations.AlterField(
            model_name='child',
            name='color',
            field=models.CharField(max_length=1, blank=True, default='', choices=[('R', 'Red'), ('G', 'Green'), ('B', 'Blue')]),
        ),
    ]
