# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Book.download_file'
        db.delete_column(u'shop_book', 'download_file')

        # Adding model 'Payment'
        db.create_table(u'shop_payment', (
            # (u'id', self.gf('django.db.models.fields.AutoField')
            #  (primary_key=True)),
            ('paymentid', self.gf('django.db.models.fields.CharField')
             (primary_key=True, max_length=100)),
            ('datecreated',
             self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('dateprocessed',
             self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('status', self.gf('django.db.models.fields.CharField')
             (default='unpaid', max_length=100, blank=True)),
            ('paid_via', self.gf('django.db.models.fields.CharField')
             (max_length=100, null=True, blank=True)),

            ('amount', self.gf('django.db.models.fields.FloatField')
             (null=True, blank=True)),
        ))
        db.send_create_signal(u'shop', ['Payment'])

        # Adding M2M table for field files on 'Payment'
        m2m_table_name = db.shorten_name(u'shop_payment_files')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID',
             primary_key=True, auto_created=True)),
            ('payment', models.ForeignKey(orm[u'shop.payment'], null=False)),
            ('bookfile', models.ForeignKey(orm[u'shop.bookfile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['payment_id', 'bookfile_id'])

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for
        # 'Book.download_file'
        raise RuntimeError(
            "Cannot reverse this migration. 'Book.download_file' and its values cannot be restored.")

        # The following code is provided here to aid in writing a correct
        # migration        # Adding field 'Book.download_file'
        db.add_column(u'shop_book', 'download_file',
                      self.gf('django.db.models.fields.files.FileField')(
                          max_length=100),
                      keep_default=False)

        # Removing M2M table for field files on 'Payment'
        db.delete_table(db.shorten_name(u'shop_payment_files'))

    models = {
        u'shop.author': {
            'Meta': {'object_name': 'Author'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'shop.book': {
            'Meta': {'object_name': 'Book'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Author']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Category']", 'null': 'True', 'blank': 'True'}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'shop.bookfile': {
            'Meta': {'object_name': 'BookFile'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'files'", 'to': u"orm['shop.Book']"}),
            'bookfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'shop.category': {
            'Meta': {'object_name': 'Category'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'categories'", 'to': u"orm['shop.Author']"}),
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
            'files': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['shop.BookFile']", 'null': 'True', 'blank': 'True'}),
            'paid_via': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'paymentid': ('django.db.models.fields.CharField', [], {'default': '675510209', 'max_length': '20', 'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'unpaid'", 'max_length': '100', 'blank': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'token_expires': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        }
    }

    complete_apps = ['shop']
