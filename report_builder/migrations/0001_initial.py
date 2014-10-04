# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisplayField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(max_length=2000, blank=True)),
                ('path_verbose', models.CharField(max_length=2000, blank=True)),
                ('field', models.CharField(max_length=2000)),
                ('field_verbose', models.CharField(max_length=2000)),
                ('name', models.CharField(max_length=2000)),
                ('sort', models.IntegerField(null=True, blank=True)),
                ('sort_reverse', models.BooleanField(default=False, verbose_name='Reverse')),
                ('width', models.IntegerField(default=15)),
                ('aggregate', models.CharField(blank=True, max_length=5, choices=[('Sum', 'Sum'), ('Count', 'Count'), ('Avg', 'Avg'), ('Max', 'Max'), ('Min', 'Min')])),
                ('position', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('total', models.BooleanField(default=False)),
                ('group', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['position'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FilterField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(max_length=2000, blank=True)),
                ('path_verbose', models.CharField(max_length=2000, blank=True)),
                ('field', models.CharField(max_length=2000)),
                ('field_verbose', models.CharField(max_length=2000)),
                ('filter_type', models.CharField(default='icontains', max_length=20, blank=True, choices=[('exact', 'Equals'), ('iexact', 'Equals (case-insensitive)'), ('contains', 'Contains'), ('icontains', 'Contains (case-insensitive)'), ('in', 'in (comma seperated 1,2,3)'), ('gt', 'Greater than'), ('gte', 'Greater than equals'), ('lt', 'Less than'), ('lte', 'Less than equals'), ('startswith', 'Starts with'), ('istartswith', 'Starts with (case-insensitive)'), ('endswith', 'Ends with'), ('iendswith', 'Ends with  (case-insensitive)'), ('range', 'range'), ('week_day', 'Week day'), ('isnull', 'Is null'), ('regex', 'Regular Expression'), ('iregex', 'Reg. Exp. (case-insensitive)')])),
                ('filter_value', models.CharField(max_length=2000)),
                ('filter_value2', models.CharField(max_length=2000, blank=True)),
                ('exclude', models.BooleanField(default=False)),
                ('position', models.PositiveSmallIntegerField(null=True, blank=True)),
            ],
            options={
                'ordering': ['position'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Format',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default='', max_length=50, blank=True)),
                ('string', models.CharField(default='', help_text='Python string format. Ex ${} would place a $ in front of the result.', max_length=300, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(verbose_name='Short Name')),
                ('description', models.TextField(blank=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('modified', models.DateField(auto_now=True)),
                ('distinct', models.BooleanField(default=False)),
                ('report_file', models.FileField(upload_to='report_files', blank=True)),
                ('report_file_creation', models.DateTimeField(null=True, blank=True)),
                ('root_model', models.ForeignKey(to='contenttypes.ContentType')),
                ('starred', models.ManyToManyField(help_text='These users have starred this report for easy reference.', related_name='report_starred_set', to=settings.AUTH_USER_MODEL, blank=True)),
                ('user_created', models.ForeignKey(blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_modified', models.ForeignKey(related_name='report_modified_set', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='filterfield',
            name='report',
            field=models.ForeignKey(to='report_builder.Report'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='displayfield',
            name='display_format',
            field=models.ForeignKey(blank=True, to='report_builder.Format', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='displayfield',
            name='report',
            field=models.ForeignKey(to='report_builder.Report'),
            preserve_default=True,
        ),
    ]
