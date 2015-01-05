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
                ('sort_reverse', models.BooleanField(default=False, verbose_name=b'Reverse')),
                ('width', models.IntegerField(default=15)),
                ('aggregate', models.CharField(blank=True, max_length=5, choices=[(b'Sum', b'Sum'), (b'Count', b'Count'), (b'Avg', b'Avg'), (b'Max', b'Max'), (b'Min', b'Min')])),
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
                ('filter_type', models.CharField(default=b'icontains', max_length=20, blank=True, choices=[(b'exact', b'Equals'), (b'iexact', b'Equals (case-insensitive)'), (b'contains', b'Contains'), (b'icontains', b'Contains (case-insensitive)'), (b'in', b'in (comma seperated 1,2,3)'), (b'gt', b'Greater than'), (b'gte', b'Greater than equals'), (b'lt', b'Less than'), (b'lte', b'Less than equals'), (b'startswith', b'Starts with'), (b'istartswith', b'Starts with (case-insensitive)'), (b'endswith', b'Ends with'), (b'iendswith', b'Ends with  (case-insensitive)'), (b'range', b'range'), (b'week_day', b'Week day'), (b'isnull', b'Is null'), (b'regex', b'Regular Expression'), (b'iregex', b'Reg. Exp. (case-insensitive)')])),
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
                ('name', models.CharField(default=b'', max_length=50, blank=True)),
                ('string', models.CharField(default=b'', help_text=b'Python string format. Ex ${} would place a $ in front of the result.', max_length=300, blank=True)),
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
                ('slug', models.SlugField(verbose_name=b'Short Name')),
                ('description', models.TextField(blank=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('modified', models.DateField(auto_now=True)),
                ('distinct', models.BooleanField(default=False)),
                ('report_file', models.FileField(upload_to=b'report_files', blank=True)),
                ('report_file_creation', models.DateTimeField(null=True, blank=True)),
                ('root_model', models.ForeignKey(to='contenttypes.ContentType')),
                ('starred', models.ManyToManyField(help_text=b'These users have starred this report for easy reference.', related_name='report_starred_set', to=settings.AUTH_USER_MODEL, blank=True)),
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
