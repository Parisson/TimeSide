# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Item'
        db.create_table('timeside_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256)),
            ('media_file', self.gf('django.db.models.fields.files.FileField')(max_length=1024, db_column='file')),
        ))
        db.send_create_signal('timeside', ['Item'])

        # Adding model 'Analysis'
        db.create_table('timeside_analysis', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='analysis', null=True, on_delete=models.SET_NULL, to=orm['timeside.Item'])),
            ('hdf5_file', self.gf('django.db.models.fields.files.FileField')(max_length=1024, db_column='hdf5')),
        ))
        db.send_create_signal('timeside', ['Analysis'])


    def backwards(self, orm):
        # Deleting model 'Item'
        db.delete_table('timeside_item')

        # Deleting model 'Analysis'
        db.delete_table('timeside_analysis')


    models = {
        'timeside.analysis': {
            'Meta': {'object_name': 'Analysis'},
            'hdf5_file': ('django.db.models.fields.files.FileField', [], {'max_length': '1024', 'db_column': "'hdf5'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'analysis'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['timeside.Item']"})
        },
        'timeside.item': {
            'Meta': {'ordering': "['code']", 'object_name': 'Item'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media_file': ('django.db.models.fields.files.FileField', [], {'max_length': '1024', 'db_column': "'file'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'})
        }
    }

    complete_apps = ['timeside']