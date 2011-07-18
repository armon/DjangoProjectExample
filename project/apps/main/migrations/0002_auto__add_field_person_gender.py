# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Person.gender'
        db.add_column('main_person', 'gender', self.gf('django.db.models.fields.CharField')(default=None, max_length=6), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Person.gender'
        db.delete_column('main_person', 'gender')


    models = {
        'main.person': {
            'Meta': {'object_name': 'Person'},
            'age': ('django.db.models.fields.IntegerField', [], {'max_length': '512'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'})
        }
    }

    complete_apps = ['main']
