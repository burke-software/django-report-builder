# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demo_models', '0009_auto_20151209_2136'),
    ]

    operations = [
        migrations.AddField(
            model_name='bar',
            name='status',
            field=models.PositiveIntegerField(default=0, choices=[(0, b'Pending'), (1, b'Approved'), (2, b'Rejected')]),
        ),
    ]
