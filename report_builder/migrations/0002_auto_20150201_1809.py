# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('report_builder', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='displayfield',
            name='aggregate',
            field=models.CharField(choices=[('Sum', 'Sum'), ('Count', 'Count'), ('Avg', 'Avg'), ('Max', 'Max'), ('Min', 'Min')], blank=True, max_length=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='displayfield',
            name='sort_reverse',
            field=models.BooleanField(default=False, verbose_name='Reverse'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='filterfield',
            name='filter_type',
            field=models.CharField(blank=True, default='icontains', choices=[('exact', 'Equals'), ('iexact', 'Equals (case-insensitive)'), ('contains', 'Contains'), ('icontains', 'Contains (case-insensitive)'), ('in', 'in (comma seperated 1,2,3)'), ('gt', 'Greater than'), ('gte', 'Greater than equals'), ('lt', 'Less than'), ('lte', 'Less than equals'), ('startswith', 'Starts with'), ('istartswith', 'Starts with (case-insensitive)'), ('endswith', 'Ends with'), ('iendswith', 'Ends with  (case-insensitive)'), ('range', 'range'), ('week_day', 'Week day'), ('isnull', 'Is null'), ('regex', 'Regular Expression'), ('iregex', 'Reg. Exp. (case-insensitive)')], max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='format',
            name='name',
            field=models.CharField(blank=True, default='', max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='format',
            name='string',
            field=models.CharField(blank=True, default='', help_text='Python string format. Ex ${} would place a $ in front of the result.', max_length=300),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='report_file',
            field=models.FileField(upload_to='report_files', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='slug',
            field=models.SlugField(verbose_name='Short Name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='starred',
            field=models.ManyToManyField(help_text='These users have starred this report for easy reference.', blank=True, related_name='report_starred_set', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
