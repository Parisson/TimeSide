# -*- coding: utf-8 -*-

from django.db.models import *
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

import uuid
import timeside

from timeside.analyzer.core import AnalyzerResultContainer
from jsonfield import JSONField


app = 'timeside'

processors = timeside.core.processors(timeside.api.IProcessor) 

STATUS = ((0, _('broken')), (1, _('pending')), (2, _('processing')),
                         (3, _('done')), (4, _('ready')))

PROCESSOR_TYPES = (('none', _('none')), ('decoder', _('decoder')), ('analyzer', _('analyzer')),
                   ('grapher', _('grapher')), ('encoder', _('encoder')))


def get_mime_type(self, path):
    return mimetypes.guess_type(path)[0]


def get_processor(self, pid):
    for proc in processors:
        if proc.id == pid:
            return proc()
    raise ValueError('Processor %s does not exists' % pid) 


class MetaCore:
    app_label = app


class Collection(Model):

    code = CharField(_('code'), unique=True, max_length=512)
    title = CharField(_('title'), blank=True, max_length=512)
    description = TextField(_('description'), blank=True)    
    items = ManyToManyField('Item', related_name="collections", verbose_name=_('items'), blank=True, null=True)

    class Meta(MetaCore):
        db_table = app + '_collections'
        ordering = ['code']
        verbose_name = _('collections')


class Media(models.Model):

    title = CharField(_('title'), blank=True, max_length=512)
    description = TextField(_('description'), blank=True)
    file = FileField(_('file'), upload_to='items/%Y/%m/%d', blank=True, max_length=1024)
    url = URLField(_('URL'), blank=True, max_length=1024)
    sha1 = CharField(_('sha1'), unique=True, blank=True, max_length=512)
    mime_type = CharField(_('mime type'), null=True, max_length=256)
    
    class Meta:
        verbose_name = _('Media')
        verbose_name_plural = _('Medias')

    def __unicode__(self):
        pass
    )

class Item(Model):

    code = CharField(_('code'), unique=True, max_length=512)
    title = CharField(_('title'), blank=True, max_length=512)
    description = TextField(_('description'), blank=True)        
    results = OneToManyField('Result', related_name="item", verbose_name=_('results'), blank=True, null=True)
    hdf5 = FileField(_('file'), upload_to='cache/%Y/%m/%d', db_column="file", max_length=1024)
    lock = BooleanField(default=False)


    class Meta(MetaCore):
        db_table = app + '_items'
        ordering = ['code']
        verbose_name = _('item')

    def __unicode__(self):
        return self.code

    def save(self, **kwargs):
        super(Item, self).save(**kwargs)
        if self.file:
            self.mime_type = get_mime_type(self.file.path)

    def results(self):
        return [result for self.experiences.all()


class Experience(Model):

    title = CharField(_('title'), blank=True, max_length=512)
    description = TextField(_('description'), blank=True)
    date_added = DateTimeField(_('date added'), auto_now_add=True)
    date_modified = DateTimeField(_('date modified'), auto_now=True, null=True)
    status = IntegerField(_('status'), choices=STATUS, default=1)
    uuid = CharField(_('uuid'), max_length=512)
    author = ForeignKey(User, related_name="experience", verbose_name=_('author'), blank=True, null=True, on_delete=models.SET_NULL)
    processors = ManyToManyField('Processor', related_name="experience", verbose_name=_('processors'), blank=True, null=True)
    
    class Meta(MetaCore):
        db_table = app + '_experiences'
        verbose_name = _('experience')

    def save(self, **kwargs):
        super(Experience, self).save(**kwargs)
        if not self.uuid:
            self.uuid = uuid.uuid4()

    def run(self, collection):        
        for item in collection.item.all():
            item.experiences.add(self)
            path = settings.MEDIA_ROOT + 'results' + os.sep + item.code + os.sep
            item.hdf5 =  path + item.code + '.hdf5'

            pipe = FileDecoder(item.file)
            proc_dict = {}
            for processor in self.processors:
                proc = get_processor(processor.id)
                #TODO: add parameters
                proc_dict[processor] = proc
                pipe = pipe | proc
            
            while item.lock:
                time.sleep(30)
    
            # pipe.run(item.hdf5)
            pipe.results.to_hdf5(item.hdf5)

            for processor in proc_dict.keys():
                proc = proc_dict[processor]
                
                results = Result.objects.filter(processor=processor, uuid=proc.UUID)

                if not results:
                    result = Result(processor=processor, uuid=proc.UUID)
                    item.results.add(result)
                else:
                    result = results[0]

                result.hdf5 = path + item.code + '_' + proc.UUID + '.hdf5'
                proc.results.to_hdf5(result.hdf5)
                result.save()
        del proc
        del pipe



class Processor(Model):
    
    pid = CharField(_('pid'), max_length=256)
    type = CharField(_('type'), choices=PROCESSOR_TYPES, default='none', max_length=64)
    parameters = JSONField(_('parameters'), blank=True)
    version = CharField(_('version'), max_length=64, blank=True)
    status = IntegerField(_('status'), choices=STATUS, default=1)
    
    class Meta(MetaCore):
        db_table = app + '_processors'
        verbose_name = _('processor')

    def save(self, **kwargs):
        super(Processor, self).save(**kwargs)
        if not self.version:
            self.version = timeside.__version__    
        if self.file:
            self.mime_type = get_mime_type(self.file.path)
        if not self.uuid:
            self.uuid = uuid.uuid4()


class Result(models.Model):

    processor = ForeignKey('Processor', related_name="experience", verbose_name=_('author'), blank=True, null=True, on_delete=models.SET_NULL)
    uuid = CharField(_('uuid'), max_length=512)
    output = FileField(_('file'), upload_to='cache/%Y/%m/%d', db_column="file", max_length=1024)
    mime_type = CharField(_('mime type'), null=True, max_length=256)
    json = JSONField(_('results'), blank=True)
    hdf5 = FileField(_('file'), upload_to='cache/%Y/%m/%d', db_column="file", max_length=1024)

    class Meta:
        verbose_name = _('Result')
        verbose_name_plural = _('Results')

    def __unicode__(self):
        pass



