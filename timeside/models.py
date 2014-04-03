# -*- coding: utf-8 -*-

import timeside, os, uuid, time, hashlib, mimetypes

from timeside.analyzer.core import AnalyzerResultContainer, AnalyzerResult

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from jsonfield import JSONField


app = 'timeside'

processors = timeside.core.processors(timeside.api.IProcessor)

PROCESSOR_PIDS = [(processor.id(), processor.id())  for processor in processors]

PROCESSOR_TYPES = (('decoder', _('decoder')), ('analyzer', _('analyzer')),
                   ('grapher', _('grapher')), ('encoder', _('encoder')))

STATUS = ((0, _('failed')), (1, _('pending')), (2, _('running')),
                         (3, _('done')), (4, _('ready')))

def get_mime_type(path):
    return mimetypes.guess_type(path)[0]


def get_processor(pid):
    for proc in processors:
        if proc.id == pid:
            return proc()
    raise ValueError('Processor %s does not exists' % pid) 


class MetaCore:

    app_label = app


class BaseResource(models.Model):

    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True, null=True)
    uuid = models.CharField(_('uuid'), blank=True, max_length=512, )

    class Meta(MetaCore):
        abstract = True
    
    def save(self, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super(BaseResource, self).save(**kwargs)


class DocumentedBaseResource(BaseResource):

    title = models.CharField(_('title'), blank=True, max_length=512)
    description = models.TextField(_('description'), blank=True)

    def __unicode__(self):
        return self.title    
    
    class Meta(MetaCore):
        abstract = True
    

class Collection(DocumentedBaseResource):

    items = models.ManyToManyField('Item', related_name="collections", verbose_name=_('items'), blank=True, null=True)

    class Meta(MetaCore):
        db_table = app + '_collections'
        ordering = ['title']
        verbose_name = _('collection')


class Item(DocumentedBaseResource):

    file = models.FileField(_('file'), upload_to='items/%Y/%m/%d', blank=True, max_length=1024)
    url = models.URLField(_('URL'), blank=True, max_length=1024)
    sha1 = models.CharField(_('sha1'), unique=True, blank=True, max_length=512)
    mime_type = models.CharField(_('mime type'), blank=True, max_length=256)
    hdf5 = models.FileField(_('HDF5 result file'), upload_to='items/%Y/%m/%d', blank=True, max_length=1024)
    lock = models.BooleanField(default=False)

    class Meta(MetaCore):
        db_table = app + '_items'
        ordering = ['title']
        verbose_name = _('item')

    def save(self, **kwargs):
        if self.file:
            self.mime_type = get_mime_type(self.file.path)
        if not self.sha1:
            pass
        super(Item, self).save(**kwargs)

    def results(self):
        return [result for result in self.results.all()]


class Experience(DocumentedBaseResource):

    processors = models.ManyToManyField('Processor', related_name="experiences", verbose_name=_('processors'), blank=True, null=True)
    author = models.ForeignKey(User, related_name="experiences", verbose_name=_('author'), blank=True, null=True, on_delete=models.SET_NULL)
    
    class Meta(MetaCore):
        db_table = app + '_experiences'
        verbose_name = _('Experience')


class Processor(BaseResource):
    
    pid = models.CharField(_('pid'), choices=PROCESSOR_PIDS, max_length=256)
    type = models.CharField(_('type'), choices=PROCESSOR_TYPES, default='none', max_length=64)
    parameters = JSONField(_('parameters'), blank=True, null=True)
    version = models.CharField(_('version'), max_length=64, blank=True)

    class Meta(MetaCore):
        db_table = app + '_processors'
        verbose_name = _('processor')

    def __unicode__(self):
        return '_'.join([self.type, self.pid, str(self.id)])
    
    def save(self, **kwargs):
        if not self.version:
            self.version = timeside.__version__
        super(Processor, self).save(**kwargs)


class Result(BaseResource):

    item = models.ForeignKey('Item', related_name="results", verbose_name=_('item'), blank=True, null=True, on_delete=models.SET_NULL)
    processor = models.ForeignKey('Processor', related_name="results", verbose_name=_('processor'), blank=True, null=True, on_delete=models.SET_NULL)
    json = JSONField(_('JSON result'), blank=True)
    hdf5 = models.FileField(_('HDF5 result file'), upload_to='results/%Y/%m/%d', blank=True, max_length=1024)
    output = models.FileField(_('Output file'), upload_to='results/%Y/%m/%d', blank=True, max_length=1024)
    output_mime_type = models.CharField(_('Output mime type'), blank=True, max_length=256)

    class Meta(MetaCore):
        db_table = app + '_results'
        verbose_name = _('Result')
        verbose_name_plural = _('Results')

    def __unicode__(self):
        return '_'.join([self.item.title, unicode(self.processor)])

    def save(self, **kwargs):
        if self.output:
            self.output_mime_type = get_mime_type(self.output.path)
        super(Result, self).save(**kwargs)


class Task(models.Model):

    experience = models.ForeignKey('Experience', related_name="task", verbose_name=_('experience'), blank=True, null=True)
    items = models.ManyToManyField('Item', related_name="task", verbose_name=_('items'), blank=True, null=True)
    status = models.IntegerField(_('status'), choices=STATUS, default=1)
    
    class Meta(MetaCore):
        db_table = app + '_tasks'
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

    def __unicode__(self):
        return '_'.join([unicode(self.experience), unicode(self.id)])

    def run(self):
        for item in self.items:
            path = settings.MEDIA_ROOT + 'results' + os.sep + item.uuid + os.sep
            if not item.hdf5:
                item.hdf5 =  path + item.uuid + '.hdf5'
            pipe = FileDecoder(item.file)
            proc_dict = {}
            for processor in self.experience.processors.all():
                proc = get_processor(processor.id)
                #TODO: add parameters
                proc_dict[processor] = proc
                pipe = pipe | proc
            while item.lock:
                time.sleep(30)
    
            pipe.run()
            pipe.results.to_hdf5(item.hdf5)

            for processor in proc_dict.keys():
                proc = proc_dict[processor]
                results = Result.objects.filter(processor=processor, uuid=proc.UUID)
                if not results:
                    result = Result(processor=processor, uuid=proc.UUID)
                    item.results.add(result)
                else:
                    result = results[0]
                result.hdf5 = path + item.uuid + '_' + proc.UUID + '.hdf5'
                proc.results.to_hdf5(result.hdf5)
                result.save()
        del proc
        del pipe
