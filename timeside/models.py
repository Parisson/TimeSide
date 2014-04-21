# -*- coding: utf-8 -*-

import timeside, os, uuid, time, hashlib, mimetypes

from timeside.analyzer.core import AnalyzerResultContainer, AnalyzerResult
from timeside.decoder.utils import sha1sum_file

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings

app = 'timeside'

processors = timeside.core.processors(timeside.api.IProcessor)

PROCESSOR_PIDS = [(processor.id(), processor.id())  for processor in processors]

STATUS = ((0, _('failed')), (1, _('pending')), (2, _('running')),
                         (3, _('done')), (4, _('ready')))

def get_mime_type(path):
    return mimetypes.guess_type(path)[0]

def get_processor(pid):
    for proc in processors:
        if proc.id() == pid:
            return proc()
    raise ValueError('Processor %s does not exists' % pid) 


class MetaCore:

    app_label = app


class BaseResource(models.Model):

    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True, null=True)
    uuid = models.CharField(_('uuid'), unique=True, blank=True, max_length=512, editable=False)

    class Meta(MetaCore):
        abstract = True
    
    def save(self, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super(BaseResource, self).save(**kwargs)


class DocBaseResource(BaseResource):

    title = models.CharField(_('title'), blank=True, max_length=512)
    description = models.TextField(_('description'), blank=True)

    def __unicode__(self):
        return self.title    
    
    class Meta(MetaCore):
        abstract = True
    

class Selection(DocBaseResource):

    items = models.ManyToManyField('Item', related_name="selections", verbose_name=_('items'), blank=True, null=True)
    author = models.ForeignKey(User, related_name="selections", verbose_name=_('author'), blank=True, null=True, on_delete=models.SET_NULL)
    selections = models.ManyToManyField('Selection', related_name="other_selections", verbose_name=_('other selections'), blank=True, null=True)

    class Meta(MetaCore):
        db_table = app + '_selections'
        verbose_name = _('selection')


class Item(DocBaseResource):

    file = models.FileField(_('file'), upload_to='items/%Y/%m/%d', blank=True, max_length=1024)
    url = models.URLField(_('URL'), blank=True, max_length=1024)
    sha1 = models.CharField(_('sha1'), blank=True, max_length=512)
    mime_type = models.CharField(_('mime type'), blank=True, max_length=256)
    hdf5 = models.FileField(_('HDF5 result file'), upload_to='items/%Y/%m/%d', blank=True, max_length=1024)
    lock = models.BooleanField(default=False)
    author = models.ForeignKey(User, related_name="items", verbose_name=_('author'), blank=True, null=True, on_delete=models.SET_NULL)

    class Meta(MetaCore):
        db_table = app + '_items'
        ordering = ['title']
        verbose_name = _('item')

    def results(self):
        return [result for result in self.results.all()]

    def lock_setter(self, lock):
        self.lock = lock
        self.save()


def update_file_properties(sender, **kwargs):
    instance = kwargs['instance']
    if instance.file:
        if not instance.mime_type:
            instance.mime_type = get_mime_type(instance.file.path)
        if not instance.sha1:
            instance.sha1 = sha1sum_file(instance.file.path)

post_save.connect(update_file_properties, sender=Item)


class Experience(DocBaseResource):

    processors = models.ManyToManyField('Processor', related_name="experiences", verbose_name=_('processors'), blank=True, null=True)
    author = models.ForeignKey(User, related_name="experiences", verbose_name=_('author'), blank=True, null=True, on_delete=models.SET_NULL)
    experiences = models.ManyToManyField('Experience', related_name="other_experiences", verbose_name=_('other experiences'), blank=True, null=True)
    is_preset = models.BooleanField(default=False)

    class Meta(MetaCore):
        db_table = app + '_experiences'
        verbose_name = _('Experience')


class Processor(models.Model):
    
    pid = models.CharField(_('pid'), choices=PROCESSOR_PIDS, max_length=256)
    version = models.CharField(_('version'), max_length=64, blank=True)

    class Meta(MetaCore):
        db_table = app + '_processors'
        verbose_name = _('processor')

    def __unicode__(self):
        return '_'.join([self.pid, str(self.id)])
    
    def save(self, **kwargs):
        if not self.version:
            self.version = timeside.__version__
        super(Processor, self).save(**kwargs)
        

class Result(BaseResource):

    item = models.ForeignKey('Item', related_name="results", verbose_name=_('item'), blank=True, null=True, on_delete=models.SET_NULL)
    processor = models.ForeignKey('Processor', related_name="results", verbose_name=_('processor'), blank=True, null=True, on_delete=models.SET_NULL)
    hdf5 = models.FileField(_('HDF5 result file'), upload_to='results/%Y/%m/%d', blank=True, max_length=1024)
    output = models.FileField(_('Output file'), upload_to='results/%Y/%m/%d', blank=True, max_length=1024)
    output_mime_type = models.CharField(_('Output mime type'), blank=True, max_length=256)
    status = models.IntegerField(_('status'), choices=STATUS, default=1)
    
    class Meta(MetaCore):
        db_table = app + '_results'
        verbose_name = _('Result')
        verbose_name_plural = _('Results')

    def status_setter(self, status):
        self.status = status
        self.save()

    def __unicode__(self):
        return '_'.join([self.item.title, unicode(self.processor)])

    def save(self, **kwargs):
        if self.output:
            self.output_mime_type = get_mime_type(self.output.path)
        super(Result, self).save(**kwargs)


class Parameters(models.Model):

    processor = models.ForeignKey('Processor', related_name="parameters", verbose_name=_('processor'), blank=True, null=True)
    parameters = models.TextField(_('Parameters'), blank=True)
    is_preset = models.BooleanField(default=False)

    class Meta:
        db_table = app + '_parameters'
        verbose_name = _('Parameters')
        verbose_name_plural = _('Parameters')

    def __unicode__(self):
        pass

    
class Task(models.Model):

    experience = models.ForeignKey('Experience', related_name="task", verbose_name=_('experience'), blank=True, null=True)
    selection = models.ForeignKey('Selection', related_name="task", verbose_name=_('selection'), blank=True, null=True)
    status = models.IntegerField(_('status'), choices=STATUS, default=1)
    author = models.ForeignKey(User, related_name="tasks", verbose_name=_('author'), blank=True, null=True, on_delete=models.SET_NULL)    

    class Meta(MetaCore):
        db_table = app + '_tasks'
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

    def __unicode__(self):
        return '_'.join([unicode(self.experience), unicode(self.id)])

    def status_setter(self, status):
        self.status = status
        self.save()

    def run(self):
        results_root = settings.MEDIA_ROOT + 'results'
        if not os.path.exists(results_root):
            os.makedirs(results_root)

        self.status_setter(2)

        for item in self.selection.items.all():
            path = results_root + os.sep + item.uuid + os.sep
            pipe = timeside.decoder.FileDecoder(item.file.path)
            proc_dict = {}

            for processor in self.experience.processors.all():
                proc = get_processor(processor.pid)
                #TODO: add parameters
                proc_dict[processor] = proc
                pipe = pipe | proc

            while item.lock:
                time.sleep(30)
            
            if not item.hdf5:
                item.hdf5 =  path + item.uuid + '.hdf5'
                item.save()
            
        
            item.lock_setter(True)
            pipe.run()
            pipe.results.to_hdf5(item.hdf5)
            item.lock_setter(False)
            
            for processor in proc_dict.keys():
                proc = proc_dict[processor]
                if proc.type == 'analyzer':
                    result = Result.objects.get_or_create(processor=processor, uuid=proc.UUID, item=item)
                    result.hdf5 = path + item.uuid + '_' + proc.UUID + '.hdf5'
                    proc.results.to_hdf5(result.hdf5)
                    result.save()
        
            # except:
            #     self.status_setter(0)
            #     item.lock_setter(False)
            #     break
        
        self.status_setter(3)
        del proc
        del pipe

