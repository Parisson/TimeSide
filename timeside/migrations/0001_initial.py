# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Collection'
        db.create_table('timeside_collections', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=512)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('timeside', ['Collection'])

        # Adding M2M table for field items on 'Collection'
        m2m_table_name = db.shorten_name('timeside_collections_items')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('collection', models.ForeignKey(orm['timeside.collection'], null=False)),
            ('item', models.ForeignKey(orm['timeside.item'], null=False))
        ))
        db.create_unique(m2m_table_name, ['collection_id', 'item_id'])

        # Adding model 'Item'
        db.create_table('timeside_items', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=512)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=1024, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=1024, blank=True)),
            ('sha1', self.gf('django.db.models.fields.CharField')(unique=True, max_length=512, blank=True)),
            ('mime_type', self.gf('django.db.models.fields.CharField')(max_length=256, null=True)),
        ))
        db.send_create_signal('timeside', ['Item'])

        # Adding M2M table for field experiences on 'Item'
        m2m_table_name = db.shorten_name('timeside_items_experiences')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('item', models.ForeignKey(orm['timeside.item'], null=False)),
            ('experience', models.ForeignKey(orm['timeside.experience'], null=False))
        ))
        db.create_unique(m2m_table_name, ['item_id', 'experience_id'])

        # Adding model 'Experience'
        db.create_table('timeside_experiences', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='experience', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
        ))
        db.send_create_signal('timeside', ['Experience'])

        # Adding M2M table for field processors on 'Experience'
        m2m_table_name = db.shorten_name('timeside_experiences_processors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('experience', models.ForeignKey(orm['timeside.experience'], null=False)),
            ('processor', models.ForeignKey(orm['timeside.processor'], null=False))
        ))
        db.create_unique(m2m_table_name, ['experience_id', 'processor_id'])

        # Adding model 'Processor'
        db.create_table('timeside_processors', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pid', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('type', self.gf('django.db.models.fields.CharField')(default='none', max_length=64)),
            ('parameters', self.gf('jsonfield.fields.JSONField')(blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=1024, db_column='file')),
            ('mime_type', self.gf('django.db.models.fields.CharField')(max_length=256, null=True)),
            ('results', self.gf('jsonfield.fields.JSONField')(blank=True)),
        ))
        db.send_create_signal('timeside', ['Processor'])


    def backwards(self, orm):
        # Deleting model 'Collection'
        db.delete_table('timeside_collections')

        # Removing M2M table for field items on 'Collection'
        db.delete_table(db.shorten_name('timeside_collections_items'))

        # Deleting model 'Item'
        db.delete_table('timeside_items')

        # Removing M2M table for field experiences on 'Item'
        db.delete_table(db.shorten_name('timeside_items_experiences'))

        # Deleting model 'Experience'
        db.delete_table('timeside_experiences')

        # Removing M2M table for field processors on 'Experience'
        db.delete_table(db.shorten_name('timeside_experiences_processors'))

        # Deleting model 'Processor'
        db.delete_table('timeside_processors')


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
        'timeside.collection': {
            'Meta': {'ordering': "['code']", 'object_name': 'Collection', 'db_table': "'timeside_collections'"},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'collections'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['timeside.Item']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'})
        },
        'timeside.experience': {
            'Meta': {'object_name': 'Experience', 'db_table': "'timeside_experiences'"},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'experience'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'processors': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'experience'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['timeside.Processor']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        'timeside.item': {
            'Meta': {'ordering': "['code']", 'object_name': 'Item', 'db_table': "'timeside_items'"},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'experiences': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'items'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['timeside.Experience']"}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '1024', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'}),
            'sha1': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '1024', 'blank': 'True'})
        },
        'timeside.processor': {
            'Meta': {'object_name': 'Processor', 'db_table': "'timeside_processors'"},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '1024', 'db_column': "'file'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'}),
            'parameters': ('jsonfield.fields.JSONField', [], {'blank': 'True'}),
            'pid': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'results': ('jsonfield.fields.JSONField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'none'", 'max_length': '64'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'})
        }
    }

    complete_apps = ['timeside']