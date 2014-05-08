# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.


class Page(models.Model):

    title = models.CharField(max_length=50)
    url = models.SlugField()
    html = models.TextField()

    class Meta:
        verbose_name = ('Отдельностоящая страница')
        verbose_name_plural = ('Отдельностоящие страницы')

    def __unicode__(self):
        return self.title
