# -*- coding: utf-8 -*-
from django.db import models
from solo.models import SingletonModel


class Homepage(SingletonModel):
    title = models.CharField(max_length=50, null=True)
    subtitle = models.CharField(max_length=50, null=True)
    description = models.TextField()

    class Meta:

        verbose_name = (u'Главная страница')
        verbose_name_plural = (u'Главная страница')
