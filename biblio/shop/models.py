
# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.core.mail import EmailMessage

import json
import os
import random
import uuid
from datetime import datetime, timedelta
from taggit.managers import TaggableManager
from taggit.models import Tag, TaggedItem
from .translit import transliterate


class Author(models.Model):

    order = models.IntegerField()
    name = models.CharField(max_length=200, help_text=u"Имя автора")
    slug = models.SlugField(
        max_length=50, help_text=u"Короткое имя английскими буквами для адресной строки")
    photo = models.ImageField(
        upload_to='authors/', help_text=u"Фотография автора, любого размера (но желательно квадратная), в формате JPG")
    thumb = ImageSpecField(source='photo',
                           processors=[ResizeToFill(100, 100)],
                           format='JPEG',
                           options={'quality': 70})
    description = models.CharField(
        max_length=300, help_text=u"Описание (пойдет на первую страницу в полосу 'наши авторы')")
    #page = models.TextField()
    #kassa = models.CharField(max_length=60)

    def get_absolute_url(self):
        return "/shop/%s" % self.slug

    class Meta:
        ordering = ['order']
        verbose_name = (u'Автор')
        verbose_name_plural = (u'Авторы')

    def __unicode__(self):
        return self.name


class Category(models.Model):

    title = models.CharField(max_length=200, help_text=u"Название категории")
    slug = models.SlugField(
        max_length=50, help_text=u"Короткое название английскими буквами для адресной строки")
    author = models.ForeignKey(Author, related_name='categories')

    class Meta:
        verbose_name = (u'Раздел')
        verbose_name_plural = (u'Разделы')

    def __unicode__(self):
        return self.title + ' (' + self.author.name + ')'

    def get_absolute_url(self):
        return "/shop/{0}/{1}".format(self.author.slug, self.slug)


class BookTag(Tag):

    class Meta:
        proxy = True

    def slugify(self, tag, i=None):
        slug = tag.lower().replace(' ', '-')
        if i is not None:
            slug += '-%d' % i
        return transliterate(slug)


class BookTaggedItem(TaggedItem):

    class Meta:
        proxy = True

    @classmethod
    def tag_model(cls):
        return BookTag


class Book(models.Model):

    title = models.CharField(max_length=200, help_text=u"Название книги")
    slug = models.SlugField(
        max_length=50, help_text=u"Короткое название английскими буквами для адресной строки")
    description = models.TextField(help_text=u"Описание/Аннотация")
    pages = models.CharField(
        blank=True, null=True, max_length=100, help_text=u"Объем книги (необязательно)")
    author = models.ForeignKey(Author, help_text=u"Автор")
    category = models.ForeignKey(
        Category, null=True, blank=True, help_text=u"Раздел (необязательно)")
    example_file = models.FileField(
        upload_to='examplefiles/', null=True, blank=True, help_text=u"Ознакомительный фрагмент (необязательно)")
    cover = models.ImageField(
        upload_to='covers/', help_text=u"Обложка, файл JPG, не меньше чем 300 на 400 пикселей")
    cover_shoplist = ImageSpecField(source='cover',
                                    processors=[ResizeToFill(140, 180)],
                                    format='JPEG',
                                    options={'quality': 80})
    cover_cart = ImageSpecField(source='cover',
                                processors=[ResizeToFill(60, 80)],
                                format='JPEG',
                                options={'quality': 80})
    cover_full = ImageSpecField(source='cover',
                                processors=[ResizeToFill(300, 400)],
                                format='JPEG',
                                options={'quality': 80})
    cover_hp = ImageSpecField(source='cover',
                              processors=[ResizeToFill(200, 290)],
                              format='JPEG',
                              options={'quality': 80})

    price = models.IntegerField(help_text=u"Цена")
    tags = TaggableManager(through=BookTaggedItem)

    def get_extension_variants(self):
        ext_list = []
        for x in self.files.all():
            ext_list.append(x.extension())
        return ext_list

    def to_JSON(self):
        return {'title': self.title, 'author': self.author.name, 'price': self.price, 'book_id': self.id, 'cover': self.cover_cart.url, 'variants': self.get_extension_variants()}

    def get_absolute_url(self):
        return "/shop/books/{0}".format(self.slug)

    def get_book_admin_page(self):

        return '<a href="%s">%s</a>' % (reverse('admin:shop_book_change', args=(self.id,)), self.title)

    get_book_admin_page.allow_tags = True

    class Meta:

        verbose_name = (u'Книга')
        verbose_name_plural = (u'Книги')

    def __unicode__(self):
        return self.title


class BookFile(models.Model):

    bookfile = models.FileField(upload_to='files/', max_length=100)

    book = models.ForeignKey(Book, related_name='files')

    def extension(self):
        name, extension = os.path.splitext(self.bookfile.name)
        return extension

    class Meta:
        verbose_name = ('Файл')
        verbose_name_plural = ('Файлы')

    def __unicode__(self):
        return self.bookfile.name

    # если обновляется файл, рассылаем новый файл покупателям
    def save(self, *args, **kw):

        if self.pk is not None:
            orig = BookFile.objects.get(pk=self.pk)
            all_emails = []
            if orig.bookfile != self.bookfile:
                super(BookFile, self).save()
                for payment in self.payments.all():
                    if payment.email not in all_emails:
                        all_emails.append(payment.email)
                        msg = EmailMessage(
                            'Обновление книги из магазина Библиоленд', 'Здравствуйте! Файл, который Вы купили, был обновлен.', 'shop@biblio.land', [payment.email])
                        msg.attach_file(self.bookfile.path)
                        msg.send()

        super(BookFile, self).save(*args, **kw)


class Payment(models.Model):

    def pkgen():
        random.seed()
        return int(str(random.random())[3:12])

    paymentid = models.CharField(
        max_length=20, primary_key=True, default=pkgen)
    datecreated = models.DateTimeField(
        null=True, auto_now=True, auto_now_add=True)
    dateprocessed = models.DateTimeField(
        null=True, auto_now=False, auto_now_add=False)
    status = models.CharField(blank=True, default='unpaid', max_length=100)
    paid_via = models.CharField(blank=True, null=True, max_length=100)
    books = models.ManyToManyField(Book, null=True, blank=True)
    files = models.ManyToManyField(
        BookFile, null=True, blank=True, related_name='payments')
    amount = models.FloatField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    token = models.CharField(null=True, blank=True, max_length=30)
    token_expires = models.DateTimeField(
        null=True, auto_now=False, auto_now_add=False)
    link_activated = models.BooleanField(default=False)

    def generate_token(self):
        self.token = str(os.urandom(30).encode('hex'))[:29]
        self.token_expires = datetime.now() + timedelta(hours=2)
        self.save(force_update=True)

    def get_link(self):

        return "/download/{0}".format(self.token)

    def get_amount(self):
        amount = 0
        for x in self.books.all():
            amount += x.price
        return amount

    def get_description(self):
        description = ''
        for x in self.books.all():
            description += x.title + ' (' + x.author.name + ')<br>'
        return description

    def get_status(self):
        if self.status == 'success':
            return u'оплачен'
        elif self.status == 'canceled':
            return u'отменен'
        elif self.status == 'waitAccept':
            return u'ожидает подтверждения платежной системы'
        else:
            return u'произошла ошибка'

    class Meta:

        verbose_name = (u'Платеж')
        verbose_name_plural = (u'Платежи')
        ordering = ['-datecreated']

    def __unicode__(self):
        return self.paymentid

