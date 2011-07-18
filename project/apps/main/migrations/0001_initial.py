# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Person'
        db.create_table('main_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, db_index=True)),
            ('age', self.gf('django.db.models.fields.IntegerField')(max_length=512)),
        ))
        db.send_create_signal('main', ['Person'])


    def backwards(self, orm):
        
        # Deleting model 'Person'
        db.delete_table('main_person')


    models = {
        'main.person': {
            'Meta': {'object_name': 'Person'},
            'age': ('django.db.models.fields.IntegerField', [], {'max_length': '512'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'})
        }
    }

    complete_apps = ['main']
