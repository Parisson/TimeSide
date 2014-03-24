# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Decoder'
        db.create_table('timeside_decoders', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pid', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('parameters', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('timeside', ['Decoder'])

        # Adding field 'Experience.decoder'
        db.add_column('timeside_experiences', 'decoder',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='experience', null=True, to=orm['timeside.Decoder']),
                      keep_default=False)

        # Adding field 'Experience.json'
        db.add_column('timeside_experiences', 'json',
                      self.gf('django.db.models.fields.files.FileField')(default=1, max_length=1024, db_column='json'),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Decoder'
        db.delete_table('timeside_decoders')

        # Deleting field 'Experience.decoder'
        db.delete_column('timeside_experiences', 'decoder_id')

        # Deleting field 'Experience.json'
        db.delete_column('timeside_experiences', 'json')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'timeside.analyzer': {
            'Meta': {'object_name': 'Analyzer', 'db_table': "'timeside_analyzers'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parameters': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'pid': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'})
        },
        'timeside.decoder': {
            'Meta': {'object_name': 'Decoder', 'db_table': "'timeside_decoders'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parameters': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'pid': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'})
        },
        'timeside.encoder': {
            'Meta': {'object_name': 'Encoder', 'db_table': "'timeside_encoders'"},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '1024', 'db_column': "'file'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'}),
            'parameters': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'pid': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'})
        },
        'timeside.experience': {
            'Meta': {'object_name': 'Experience', 'db_table': "'timeside_experiences'"},
            'analyzers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'experience'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['timeside.Analyzer']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'experience'", 'null': 'True', 'to': "orm['auth.User']"}),
            'begin_time': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'decoder': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'experience'", 'null': 'True', 'to': "orm['timeside.Decoder']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'encoders': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'experience'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['timeside.Encoder']"}),
            'end_time': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'graphers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'experience'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['timeside.Grapher']"}),
            'hdf5': ('django.db.models.fields.files.FileField', [], {'max_length': '1024', 'db_column': "'hdf5'"}),
            'high_frequency': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'experience'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['timeside.Item']"}),
            'json': ('django.db.models.fields.files.FileField', [], {'max_length': '1024', 'db_column': "'json'"}),
            'low_frequency': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'timeside.grapher': {
            'Meta': {'object_name': 'Grapher', 'db_table': "'timeside_graphers'"},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '1024', 'db_column': "'file'"}),
            'height': ('django.db.models.fields.IntegerField', [], {'default': '180'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'}),
            'parameters': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'pid': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {'default': '320'})
        },
        'timeside.item': {
            'Meta': {'ordering': "['code']", 'object_name': 'Item', 'db_table': "'timeside_items'"},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '1024', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'}),
            'sha1': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '1024', 'blank': 'True'})
        }
    }

    complete_apps = ['timeside']