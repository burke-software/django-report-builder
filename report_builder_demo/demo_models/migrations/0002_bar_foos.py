# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demo_models', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bar',
            name='foos',
            field=models.ManyToManyField(blank=True, to='demo_models.Foo'),
            preserve_default=True,
        ),
    ]
