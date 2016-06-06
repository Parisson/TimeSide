# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Selection'
        db.create_table('timeside_selections', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=512, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='selections', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
        ))
        db.send_create_signal('server', ['Selection'])

        # Adding M2M table for field items on 'Selection'
        m2m_table_name = db.shorten_name('timeside_selections_items')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('selection', models.ForeignKey(orm['server.selection'], null=False)),
            ('item', models.ForeignKey(orm['server.item'], null=False))
        ))
        db.create_unique(m2m_table_name, ['selection_id', 'item_id'])

        # Adding M2M table for field selections on 'Selection'
        m2m_table_name = db.shorten_name('timeside_selections_selections')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_selection', models.ForeignKey(orm['server.selection'], null=False)),
            ('to_selection', models.ForeignKey(orm['server.selection'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_selection_id', 'to_selection_id'])

        # Adding model 'Item'
        db.create_table('timeside_items', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=512, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=1024, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=1024, blank=True)),
            ('sha1', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
            ('mime_type', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('hdf5', self.gf('django.db.models.fields.files.FileField')(max_length=1024, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='items', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
            ('lock', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('server', ['Item'])

        # Adding model 'Experience'
        db.create_table('timeside_experiences', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=512, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='experiences', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('server', ['Experience'])

        # Adding M2M table for field presets on 'Experience'
        m2m_table_name = db.shorten_name('timeside_experiences_presets')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('experience', models.ForeignKey(orm['server.experience'], null=False)),
            ('preset', models.ForeignKey(orm['server.preset'], null=False))
        ))
        db.create_unique(m2m_table_name, ['experience_id', 'preset_id'])

        # Adding M2M table for field experiences on 'Experience'
        m2m_table_name = db.shorten_name('timeside_experiences_experiences')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_experience', models.ForeignKey(orm['server.experience'], null=False)),
            ('to_experience', models.ForeignKey(orm['server.experience'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_experience_id', 'to_experience_id'])

        # Adding model 'Processor'
        db.create_table('timeside_processors', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pid', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
        ))
        db.send_create_signal('server', ['Processor'])

        # Adding model 'Preset'
        db.create_table('timeside_presets', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=512, blank=True)),
            ('processor', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='presets', null=True, to=orm['server.Processor'])),
            ('parameters', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='presets', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('server', ['Preset'])

        # Adding model 'Result'
        db.create_table('timeside_results', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=512, blank=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='results', null=True, on_delete=models.SET_NULL, to=orm['server.Item'])),
            ('preset', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='results', null=True, on_delete=models.SET_NULL, to=orm['server.Preset'])),
            ('hdf5', self.gf('django.db.models.fields.files.FileField')(max_length=1024, blank=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=1024, blank=True)),
            ('mime_type', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='results', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
        ))
        db.send_create_signal('server', ['Result'])

        # Adding model 'Task'
        db.create_table('timeside_tasks', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=512, blank=True)),
            ('experience', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='task', null=True, to=orm['server.Experience'])),
            ('selection', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='task', null=True, to=orm['server.Selection'])),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tasks', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
        ))
        db.send_create_signal('server', ['Task'])


    def backwards(self, orm):
        # Deleting model 'Selection'
        db.delete_table('timeside_selections')

        # Removing M2M table for field items on 'Selection'
        db.delete_table(db.shorten_name('timeside_selections_items'))

        # Removing M2M table for field selections on 'Selection'
        db.delete_table(db.shorten_name('timeside_selections_selections'))

        # Deleting model 'Item'
        db.delete_table('timeside_items')

        # Deleting model 'Experience'
        db.delete_table('timeside_experiences')

        # Removing M2M table for field presets on 'Experience'
        db.delete_table(db.shorten_name('timeside_experiences_presets'))

        # Removing M2M table for field experiences on 'Experience'
        db.delete_table(db.shorten_name('timeside_experiences_experiences'))

        # Deleting model 'Processor'
        db.delete_table('timeside_processors')

        # Deleting model 'Preset'
        db.delete_table('timeside_presets')

        # Deleting model 'Result'
        db.delete_table('timeside_results')

        # Deleting model 'Task'
        db.delete_table('timeside_tasks')


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
        'server.experience': {
            'Meta': {'object_name': 'Experience', 'db_table': "'timeside_experiences'"},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'experiences'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'experiences': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'other_experiences'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['server.Experience']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'presets': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'experiences'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['server.Preset']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512', 'blank': 'True'})
        },
        'server.item': {
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
        'server.preset': {
            'Meta': {'object_name': 'Preset', 'db_table': "'timeside_presets'"},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'presets'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parameters': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'processor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'presets'", 'null': 'True', 'to': "orm['server.Processor']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512', 'blank': 'True'})
        },
        'server.processor': {
            'Meta': {'object_name': 'Processor', 'db_table': "'timeside_processors'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pid': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'})
        },
        'server.result': {
            'Meta': {'object_name': 'Result', 'db_table': "'timeside_results'"},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'results'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '1024', 'blank': 'True'}),
            'hdf5': ('django.db.models.fields.files.FileField', [], {'max_length': '1024', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'results'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['server.Item']"}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'preset': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'results'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['server.Preset']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'uuid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512', 'blank': 'True'})
        },
        'server.selection': {
            'Meta': {'object_name': 'Selection', 'db_table': "'timeside_selections'"},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'selections'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'selections'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['server.Item']"}),
            'selections': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'other_selections'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['server.Selection']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512', 'blank': 'True'})
        },
        'server.task': {
            'Meta': {'object_name': 'Task', 'db_table': "'timeside_tasks'"},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tasks'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'experience': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'task'", 'null': 'True', 'to': "orm['server.Experience']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'selection': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'task'", 'null': 'True', 'to': "orm['server.Selection']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'uuid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512', 'blank': 'True'})
        }
    }

    complete_apps = ['server']