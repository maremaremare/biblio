# -*- coding: utf-8 -*-
from django.template.defaultfilters import slugify
from taggit.models import Tag, TaggedItem
# from biblio.settings.base import SLUG_TRANSLITERATOR


class RuTag(Tag):

    class Meta:
        proxy = True


def slugify(self, tag, i=None):
    return slugify(self.name)[:128]


class RuTaggedItem(TaggedItem):

    class Meta:
        proxy = True

    @classmethod
    def tag_model(cls):
        return RuTag
