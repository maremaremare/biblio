# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Payment.id'
        db.delete_column(u'shop_payment', u'id')


        # Changing field 'Payment.paymentid'
        db.alter_column(u'shop_payment', 'paymentid', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True))
        # Adding unique constraint on 'Payment', fields ['paymentid']
        db.create_unique(u'shop_payment', ['paymentid'])


    def backwards(self, orm):
        # Removing unique constraint on 'Payment', fields ['paymentid']
        db.delete_unique(u'shop_payment', ['paymentid'])

        # Adding field 'Payment.id'
        db.add_column(u'shop_payment', u'id',
                      self.gf('django.db.models.fields.AutoField')(default='lll', primary_key=True),
                      keep_default=False)


        # Changing field 'Payment.paymentid'
        db.alter_column(u'shop_payment', 'paymentid', self.gf('django.db.models.fields.IntegerField')(null=True))

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
            'books': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['shop.Book']", 'null': 'True', 'blank': 'True'}),
            'datecreated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'dateprocessed': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'paid_via': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'paymentid': ('django.db.models.fields.CharField', [], {'default': "'2a9493295d9a7cfe'", 'max_length': '20', 'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'unpaid'", 'max_length': '100', 'blank': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'token_expires': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        }
    }

    complete_apps = ['shop']