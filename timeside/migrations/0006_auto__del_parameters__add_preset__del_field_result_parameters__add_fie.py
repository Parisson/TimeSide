# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Parameters'
        db.delete_table('timeside_parameters')

        # Adding model 'Preset'
        db.create_table('timeside_presets', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('processor', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='preset', null=True, to=orm['timeside.Processor'])),
            ('parameters', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('timeside', ['Preset'])

        # Deleting field 'Result.parameters'
        db.delete_column('timeside_results', 'parameters_id')

        # Adding field 'Result.preset'
        db.add_column('timeside_results', 'preset',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='results', null=True, on_delete=models.SET_NULL, to=orm['timeside.Preset']),
                      keep_default=False)


        # Changing field 'Result.hdf5'
        db.alter_column('timeside_results', 'hdf5', self.gf('django.db.models.fields.files.FileField')(default=0, max_length=1024))

        # Changing field 'Result.file'
        db.alter_column('timeside_results', 'file', self.gf('django.db.models.fields.files.FileField')(default=0, max_length=1024))
        # Deleting field 'Experience.is_preset'
        db.delete_column('timeside_experiences', 'is_preset')

        # Adding field 'Experience.is_public'
        db.add_column('timeside_experiences', 'is_public',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Removing M2M table for field processors on 'Experience'
        db.delete_table(db.shorten_name('timeside_experiences_processors'))

        # Adding M2M table for field presets on 'Experience'
        m2m_table_name = db.shorten_name('timeside_experiences_presets')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('experience', models.ForeignKey(orm['timeside.experience'], null=False)),
            ('preset', models.ForeignKey(orm['timeside.preset'], null=False))
        ))
        db.create_unique(m2m_table_name, ['experience_id', 'preset_id'])


    def backwards(self, orm):
        # Adding model 'Parameters'
        db.create_table('timeside_parameters', (
            ('parameters', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_preset', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('processor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='parameters', null=True, to=orm['timeside.Processor'], blank=True)),
        ))
        db.send_create_signal('timeside', ['Parameters'])

        # Deleting model 'Preset'
        db.delete_table('timeside_presets')

        # Adding field 'Result.parameters'
        db.add_column('timeside_results', 'parameters',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='results', null=True, to=orm['timeside.Parameters'], on_delete=models.SET_NULL, blank=True),
                      keep_default=False)

        # Deleting field 'Result.preset'
        db.delete_column('timeside_results', 'preset_id')


        # Changing field 'Result.hdf5'
        db.alter_column('timeside_results', 'hdf5', self.gf('django.db.models.fields.files.FileField')(max_length=1024, null=True))

        # Changing field 'Result.file'
        db.alter_column('timeside_results', 'file', self.gf('django.db.models.fields.files.FileField')(max_length=1024, null=True))
        # Adding field 'Experience.is_preset'
        db.add_column('timeside_experiences', 'is_preset',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'Experience.is_public'
        db.delete_column('timeside_experiences', 'is_public')

        # Adding M2M table for field processors on 'Experience'
        m2m_table_name = db.shorten_name('timeside_experiences_processors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('experience', models.ForeignKey(orm['timeside.experience'], null=False)),
            ('processor', models.ForeignKey(orm['timeside.processor'], null=False))
        ))
        db.create_unique(m2m_table_name, ['experience_id', 'processor_id'])

        # Removing M2M table for field presets on 'Experience'
        db.delete_table(db.shorten_name('timeside_experiences_presets'))


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
        'timeside.experience': {
            'Meta': {'object_name': 'Experience', 'db_table': "'timeside_experiences'"},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'experiences'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'experiences': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'other_experiences'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['timeside.Experience']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'presets': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'experiences'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['timeside.Preset']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512', 'blank': 'True'})
        },
        'timeside.item': {
            'Meta': {'ordering': "['title']", 'object_name': 'Item', 'db_table': "'timeside_items'"},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'items'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '1024', 'blank': 'True'}),
            'hdf5': ('django.db.models.fields.files.FileField', [], {'max_length': '1024', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lock': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'sha1': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '1024', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512', 'blank': 'True'})
        },
        'timeside.preset': {
            'Meta': {'object_name': 'Preset', 'db_table': "'timeside_presets'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parameters': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'processor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'preset'", 'null': 'True', 'to': "orm['timeside.Processor']"})
        },
        'timeside.processor': {
            'Meta': {'object_name': 'Processor', 'db_table': "'timeside_processors'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pid': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'})
        },
        'timeside.result': {
            'Meta': {'object_name': 'Result', 'db_table': "'timeside_results'"},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '1024', 'blank': 'True'}),
            'hdf5': ('django.db.models.fields.files.FileField', [], {'max_length': '1024', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'results'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['timeside.Item']"}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'preset': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'results'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['timeside.Preset']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'uuid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512', 'blank': 'True'})
        },
        'timeside.selection': {
            'Meta': {'object_name': 'Selection', 'db_table': "'timeside_selections'"},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'selections'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'selections'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['timeside.Item']"}),
            'selections': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'other_selections'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['timeside.Selection']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512', 'blank': 'True'})
        },
        'timeside.task': {
            'Meta': {'object_name': 'Task', 'db_table': "'timeside_tasks'"},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tasks'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"}),
            'experience': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'task'", 'null': 'True', 'to': "orm['timeside.Experience']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'selection': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'task'", 'null': 'True', 'to': "orm['timeside.Selection']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['timeside']