# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DancerEmail'
        db.create_table('dancer_email_parser_danceremail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('raw', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('data', self.gf('django.db.models.fields.TextField')()),
            ('processed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('dancer_email_parser', ['DancerEmail'])

        # Adding model 'DancerPhone'
        db.create_table('dancer_email_parser_dancerphone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('raw', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('data', self.gf('django.db.models.fields.TextField')()),
            ('processed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('dancer_email_parser', ['DancerPhone'])


    def backwards(self, orm):
        # Deleting model 'DancerEmail'
        db.delete_table('dancer_email_parser_danceremail')

        # Deleting model 'DancerPhone'
        db.delete_table('dancer_email_parser_dancerphone')


    models = {
        'dancer_email_parser.danceremail': {
            'Meta': {'object_name': 'DancerEmail'},
            'data': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'raw': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'dancer_email_parser.dancerphone': {
            'Meta': {'object_name': 'DancerPhone'},
            'data': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'raw': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['dancer_email_parser']