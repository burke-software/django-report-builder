# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Report'
        db.create_table('report_builder_report', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('root_model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('distinct', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('report_builder', ['Report'])

        # Adding model 'DisplayField'
        db.create_table('report_builder_displayfield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['report_builder.Report'])),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=2000, blank=True)),
            ('path_verbose', self.gf('django.db.models.fields.CharField')(max_length=2000, blank=True)),
            ('field', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('field_verbose', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('sort', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('sort_reverse', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('width', self.gf('django.db.models.fields.IntegerField')(default=120)),
            ('aggregate', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('report_builder', ['DisplayField'])

        # Adding model 'FilterField'
        db.create_table('report_builder_filterfield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['report_builder.Report'])),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=2000, blank=True)),
            ('path_verbose', self.gf('django.db.models.fields.CharField')(max_length=2000, blank=True)),
            ('field', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('field_verbose', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('filter_type', self.gf('django.db.models.fields.CharField')(default='icontains', max_length=20, blank=True)),
            ('filter_value', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('filter_value2', self.gf('django.db.models.fields.CharField')(max_length=2000, blank=True)),
            ('exclude', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('report_builder', ['FilterField'])


    def backwards(self, orm):
        # Deleting model 'Report'
        db.delete_table('report_builder_report')

        # Deleting model 'DisplayField'
        db.delete_table('report_builder_displayfield')

        # Deleting model 'FilterField'
        db.delete_table('report_builder_filterfield')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'report_builder.displayfield': {
            'Meta': {'ordering': "['position']", 'object_name': 'DisplayField'},
            'aggregate': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'field': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'field_verbose': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            'path_verbose': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['report_builder.Report']"}),
            'sort': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sort_reverse': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'width': ('django.db.models.fields.IntegerField', [], {'default': '120'})
        },
        'report_builder.filterfield': {
            'Meta': {'ordering': "['position']", 'object_name': 'FilterField'},
            'exclude': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'field': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'field_verbose': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'filter_type': ('django.db.models.fields.CharField', [], {'default': "'icontains'", 'max_length': '20', 'blank': 'True'}),
            'filter_value': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'filter_value2': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            'path_verbose': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['report_builder.Report']"})
        },
        'report_builder.report': {
            'Meta': {'object_name': 'Report'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'distinct': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'root_model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"})
        }
    }

    complete_apps = ['report_builder']