# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bar',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('char_field', models.CharField(blank=True, max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Foo',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('char_field', models.CharField(blank=True, max_length=50)),
                ('char_field2', models.CharField(blank=True, max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FooExclude',
            fields=[
                ('foo_ptr', models.OneToOneField(auto_created=True, serialize=False, parent_link=True, primary_key=True, to='demo_models.Foo')),
            ],
            options={
            },
            bases=('demo_models.foo',),
        ),
    ]
