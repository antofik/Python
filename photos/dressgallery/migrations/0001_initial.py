# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Dress'
        db.create_table('dressgallery_dress', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('fio', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('height', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('svarovsky', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('cost', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('discount', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('vk', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('place', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('main_photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('main_photo_description', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('complains', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('blocked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sold', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('access_key', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('views', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('buy_tries', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rating_votes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
            ('rating_score', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
        ))
        db.send_create_signal('dressgallery', ['Dress'])

        # Adding model 'Photo'
        db.create_table('dressgallery_photo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('gallery', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('dress', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dressgallery.Dress'])),
        ))
        db.send_create_signal('dressgallery', ['Photo'])


    def backwards(self, orm):
        # Deleting model 'Dress'
        db.delete_table('dressgallery_dress')

        # Deleting model 'Photo'
        db.delete_table('dressgallery_photo')


    models = {
        'dressgallery.dress': {
            'Meta': {'ordering': "['-modified']", 'object_name': 'Dress'},
            'access_key': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'blocked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'buy_tries': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'complains': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'cost': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'discount': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'fio': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'height': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'main_photo_description': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'rating_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'rating_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'sold': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'svarovsky': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'vk': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'dressgallery.photo': {
            'Meta': {'ordering': "['dress']", 'object_name': 'Photo'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'dress': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dressgallery.Dress']"}),
            'gallery': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['dressgallery']