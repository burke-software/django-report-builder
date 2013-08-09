# -*- coding: utf-8 -*-
import datetime
import sys
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        from report_builder.models import Format
        # Create some initial data
        if sys.version_info > (2,7):
            # Doesn't work in 2.6
            Format.objects.create(
                name = "US Currency",
                string = "${:20,.2f}",
            )
            Format.objects.create(
                name = "ISO Date",
                string = "{:%Y-%m-%d}",
            )
        Format.objects.create(
            name = "Percent",
            string = "{0:.0f}%",
        )


    def backwards(self, orm):
        pass

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'report_builder.displayfield': {
            'Meta': {'ordering': "['position']", 'object_name': 'DisplayField'},
            'aggregate': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'display_format': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['report_builder.Format']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'field': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'field_verbose': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'group': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            'path_verbose': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['report_builder.Report']"}),
            'sort': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sort_reverse': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'total': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'width': ('django.db.models.fields.IntegerField', [], {'default': '15'})
        },
        u'report_builder.filterfield': {
            'Meta': {'ordering': "['position']", 'object_name': 'FilterField'},
            'exclude': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'field': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'field_verbose': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'filter_type': ('django.db.models.fields.CharField', [], {'default': "'icontains'", 'max_length': '20', 'blank': 'True'}),
            'filter_value': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'filter_value2': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            'path_verbose': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['report_builder.Report']"})
        },
        u'report_builder.format': {
            'Meta': {'object_name': 'Format'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'string': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300', 'blank': 'True'})
        },
        u'report_builder.report': {
            'Meta': {'object_name': 'Report'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'distinct': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'root_model': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'starred': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'report_starred_set'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'user_created': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'user_modified': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'report_modified_set'", 'null': 'True', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['report_builder']
