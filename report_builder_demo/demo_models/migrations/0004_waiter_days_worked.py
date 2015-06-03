# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demo_models', '0003_auto_20150419_2110'),
    ]

    operations = [
        migrations.AddField(
            model_name='waiter',
            name='days_worked',
            field=models.IntegerField(default=None, null=True, blank=True),
        ),
    ]
