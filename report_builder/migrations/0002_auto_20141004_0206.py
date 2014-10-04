# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report_builder', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportDownload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('report_file', models.FileField(upload_to='report_files', blank=True)),
                ('started', models.DateTimeField(auto_now_add=True)),
                ('finished', models.DateTimeField(null=True, blank=True)),
                ('report', models.ForeignKey(to='report_builder.Report')),
            ],
            options={
                'ordering': ('-finished',),
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='report',
            name='report_file',
        ),
        migrations.RemoveField(
            model_name='report',
            name='report_file_creation',
        ),
    ]
