# -*- coding: utf-8 -*-

from django.db.models import *
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

import timeside

app = 'timeside'

STATUS = ((0, _('broken')), (1, _('pending')), (2, _('processing')),
                         (3, _('done')), (4, _('ready')))

class MetaCore:
    app_label = app


class Item(Model):

    code = CharField(_('code'), unique=True, max_length=512)
    title = CharField(_('title'), blank=True, max_length=512)
    description = TextField(_('description'), blank=True)
    file = FileField(_('file'), upload_to='items/%Y/%m/%d', blank=True, max_length=1024)
    url = URLField(_('URL'), blank=True, max_length=1024)
    sha1 = CharField(_('sha1'), unique=True, blank=True, max_length=512)
    mime_type = CharField(_('mime_type'), null=True, max_length=256)

    def set_mime_type(self):
        if self.file:
            self.mime_type = mimetypes.guess_type(self.file.path)[0]

    class Meta(MetaCore):
        db_table = app + '_items'
        ordering = ['code']
        verbose_name = _('item')

    def __unicode__(self):
        return self.code


class Processor(Model):
    
    pid = CharField(_('pid'), max_length=256)
    parameters = TextField(_('parameters'), blank=True)
    version = CharField(_('version'), max_length=64, blank=True)
    status = IntegerField(_('status'), choices=STATUS, default=1)

    def save(self):
        super(Processor, self).save()
        if not self.version:
            self.version = timeside.__version__    

    class Meta(MetaCore):
        abstract=True


class Decoder(Processor):

    class Meta(MetaCore):
        db_table = app + '_decoders'
        verbose_name = _('decoder')


class Analyzer(Processor):

    class Meta(MetaCore):
        db_table = app + '_analyzers'
        verbose_name = _('analyzer')


class Grapher(Processor):

    file = FileField(_('file'), upload_to='cache/grapher/%Y/%m/%d', db_column="file", max_length=1024)
    mime_type = CharField(_('mime_type'), null=True, max_length=256)
    height = IntegerField(_('height'), default=180)
    width = IntegerField(_('width'), default=320)

    class Meta(MetaCore):
        db_table = app + '_graphers'
        verbose_name = _('grapher')


class Encoder(Processor):

    file = FileField(_('file'), upload_to='cache/encoder/%Y/%m/%d', db_column="file", max_length=1024)
    mime_type = CharField(_('mime_type'), null=True, max_length=256)

    class Meta(MetaCore):
        db_table = app + '_encoders'
        verbose_name = _('encoder')


class Experience(Model):

    item = ForeignKey(Item, related_name='experience', verbose_name=_('item'), null=True, on_delete=SET_NULL)    
    title = CharField(_('title'), blank=True, max_length=512)
    description = TextField(_('description'), blank=True)
    date_added = DateTimeField(_('date added'), auto_now_add=True)
    date_modified = DateTimeField(_('date modified'), auto_now=True, null=True)
    status = IntegerField(_('status'), choices=STATUS, default=1)
    uuid = CharField(_('uuid'), max_length=256)
    author = ForeignKey(User, related_name="experience", verbose_name=_('author'), blank=True, null=True)

    decoder = ForeignKey(Decoder, related_name="experience", verbose_name=_('decoder'), null=True)
    analyzers = ManyToManyField(Analyzer, related_name="experience", verbose_name=_('analyzers'), blank=True, null=True)
    graphers = ManyToManyField(Grapher, related_name="experience", verbose_name=_('graphers'), blank=True, null=True)
    encoders = ManyToManyField(Encoder, related_name="experience", verbose_name=_('encoders'), blank=True, null=True)

    begin_time = FloatField(_('begin time'), default=0, blank=True)
    end_time = FloatField(_('end time'), blank=True)
    low_frequency = FloatField(_('low frequency'), blank=True)
    high_frequency = FloatField(_('highh frequency'), blank=True)

    hdf5 = FileField(_('hdf5_file'), upload_to='cache/hdf5/%Y/%m/%d', db_column="hdf5", max_length=1024)
    json = FileField(_('json_file'), upload_to='cache/json/%Y/%m/%d', db_column="json", max_length=1024)
        
    class Meta(MetaCore):
        db_table = app + '_experiences'
        verbose_name = _('experience')

    def results(self):
        pass


