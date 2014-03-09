# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Reply.dress'
        db.alter_column('dressgallery_reply', 'dress_id', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['dressgallery.Dress']))

    def backwards(self, orm):

        # Changing field 'Reply.dress'
        db.alter_column('dressgallery_reply', 'dress_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dressgallery.Dress'], null=True))

    models = {
        'dressgallery.dress': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Dress'},
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
            'discount': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'fio': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'height': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'main_photo_description': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
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
            'vk': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'dressgallery.photo': {
            'Meta': {'ordering': "['dress']", 'object_name': 'Photo'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'dress': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dressgallery.Dress']"}),
            'gallery': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'is_main': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'dressgallery.reply': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Reply'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'dress': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dressgallery.Dress']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'email_delivered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fio': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'sms_delivered': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['dressgallery']