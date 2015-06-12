# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demo_models', '0004_waiter_days_worked'),
    ]

    operations = [
        migrations.CreateModel(
            name='Child',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('age', models.IntegerField(default=None, null=True, blank=True)),
                ('color', models.CharField(default=b'', max_length=1, blank=True, choices=[(b'R', b'Red'), (b'G', b'Green'), (b'B', b'Blue')])),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='bar',
            name='check_mate_status',
            field=models.CharField(default=b'CH', max_length=2, choices=[(b'CH', b'CHECK'), (b'MA', b'CHECKMATE')]),
        ),
        migrations.AddField(
            model_name='child',
            name='parent',
            field=models.ForeignKey(related_name='children', to='demo_models.Person'),
        ),
    ]
