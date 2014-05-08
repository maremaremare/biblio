# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Author'
        db.create_table(u'shop_author', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('page', self.gf('django.db.models.fields.TextField')()),
            ('kassa', self.gf('django.db.models.fields.CharField')(max_length=60)),
        ))
        db.send_create_signal(u'shop', ['Author'])

        # Adding model 'Category'
        db.create_table(u'shop_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Author'])),
        ))
        db.send_create_signal(u'shop', ['Category'])

        # Adding model 'Book'
        db.create_table(u'shop_book', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Author'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Category'], null=True, blank=True)),
            ('cover', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('download_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('price', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'shop', ['Book'])

        # Adding model 'Payment'
        db.create_table(u'shop_payment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('paymentid', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('datecreated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('dateprocessed', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='unpaid', max_length=100, blank=True)),
            ('paid_via', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Book'], null=True)),
            ('amount', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'shop', ['Payment'])


    def backwards(self, orm):
        # Deleting model 'Author'
        db.delete_table(u'shop_author')

        # Deleting model 'Category'
        db.delete_table(u'shop_category')

        # Deleting model 'Book'
        db.delete_table(u'shop_book')

        # Deleting model 'Payment'
        db.delete_table(u'shop_payment')


    models = {
        u'shop.author': {
            'Meta': {'object_name': 'Author'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kassa': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'page': ('django.db.models.fields.TextField', [], {}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'shop.book': {
            'Meta': {'object_name': 'Book'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Author']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Category']", 'null': 'True', 'blank': 'True'}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'download_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'shop.category': {
            'Meta': {'object_name': 'Category'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Author']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'shop.payment': {
            'Meta': {'object_name': 'Payment'},
            'amount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Book']", 'null': 'True'}),
            'datecreated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'dateprocessed': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid_via': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'paymentid': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'unpaid'", 'max_length': '100', 'blank': 'True'})
        }
    }

    complete_apps = ['shop']