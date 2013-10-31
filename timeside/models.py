# -*- coding: utf-8 -*-

from django.db.models import *
from django.utils.translation import ugettext_lazy as _


class MetaCore:
    app_label = 'timeside'


class Item(Model):

    title = CharField(_('title'), blank=True, max_length=512)
    description = CharField(_('description'), blank=True, max_length=1024)
    code = CharField(_('code'), unique=True, max_length=256)
    media_file = FileField(_('file'), upload_to='items/%Y/%m/%d',
                                      db_column="file", max_length=1024)

    class Meta(MetaCore):
        db_table = 'timeside_item'
        ordering = ['code']
        verbose_name = _('item')

    def __unicode__(self):
        return self.code


class Analysis(Model):

    item = ForeignKey(Item, related_name='analysis',
                        verbose_name=_('item'), null=True, on_delete=SET_NULL)
    hdf5_file = FileField(_('file'), upload_to='cache/%Y/%m/%d',
                        db_column="hdf5", max_length=1024)

    class Meta(MetaCore):
        db_table = 'timeside_analysis'
        verbose_name = _('analysis')

    def results(self):
        pass