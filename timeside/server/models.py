# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Parisson SARL
# Copyright (c) 2014 Guillaume Pellerin <yomguy@parisson.com>
# Copyright (c) 2014 Thomas Fillon <thomas@parisson.com>

# This file is part of TimeSide.

# TimeSide is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# TimeSide is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with TimeSide.  If not, see <http://www.gnu.org/licenses/>.

# Authors:
# Guillaume Pellerin <yomguy@parisson.com>
# Thomas Fillon <thomas@parisson.com>

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

STATUS = ((0, _('failed')), (1, _('draft')), (2, _('pending')),
                         (3, _('running')), (4, _('done')))

def get_mime_type(path):
    return mimetypes.guess_type(path)[0]

def get_processor(pid):
    for proc in processors:
        if proc.id() == pid:
            return proc
    raise ValueError('Processor %s does not exists' % pid)


class MetaCore:

    app_label = 'server'


class BaseResource(models.Model):

    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True, null=True)
    uuid = models.CharField(_('uuid'), unique=True, blank=True, max_length=512)

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
    selections = models.ManyToManyField('Selection', related_name="other_selections", verbose_name=_('other selections'), blank=True, null=True)
    author = models.ForeignKey(User, related_name="selections", verbose_name=_('author'), blank=True, null=True, on_delete=models.SET_NULL)

    class Meta(MetaCore):
        db_table = app + '_selections'
        verbose_name = _('selection')


class Item(DocBaseResource):

    element_type = 'timeside_item'

    file = models.FileField(_('file'), upload_to='items/%Y/%m/%d', blank=True, max_length=1024)
    url = models.URLField(_('URL'), blank=True, max_length=1024)
    sha1 = models.CharField(_('sha1'), blank=True, max_length=512)
    mime_type = models.CharField(_('mime type'), blank=True, max_length=256)
    hdf5 = models.FileField(_('HDF5 result file'), upload_to='results/%Y/%m/%d', blank=True, max_length=1024)
    author = models.ForeignKey(User, related_name="items", verbose_name=_('author'), blank=True, null=True, on_delete=models.SET_NULL)
    lock = models.BooleanField(default=False)

    class Meta(MetaCore):
        db_table = app + '_items'
        ordering = ['title']
        verbose_name = _('item')

    def results(self):
        return [result for result in self.results.all()]

    def lock_setter(self, lock):
        self.lock = lock
        self.save()


class Experience(DocBaseResource):

    presets = models.ManyToManyField('Preset', related_name="experiences", verbose_name=_('presets'), blank=True, null=True)
    experiences = models.ManyToManyField('Experience', related_name="other_experiences", verbose_name=_('other experiences'), blank=True, null=True)
    author = models.ForeignKey(User, related_name="experiences", verbose_name=_('author'), blank=True, null=True, on_delete=models.SET_NULL)
    is_public = models.BooleanField(default=False)

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


class Preset(BaseResource):

    processor = models.ForeignKey('Processor', related_name="presets", verbose_name=_('processor'), blank=True, null=True)
    parameters = models.TextField(_('Parameters'), blank=True)
    author = models.ForeignKey(User, related_name="presets", verbose_name=_('author'), blank=True, null=True, on_delete=models.SET_NULL)
    is_public = models.BooleanField(default=False)

    class Meta(MetaCore):
        db_table = app + '_presets'
        verbose_name = _('Preset')
        verbose_name_plural = _('Presets')

    def __unicode__(self):
        return '_'.join([unicode(self.processor), str(self.id)])


class Result(BaseResource):

    item = models.ForeignKey('Item', related_name="results", verbose_name=_('item'), blank=True, null=True, on_delete=models.SET_NULL)
    preset = models.ForeignKey('Preset', related_name="results", verbose_name=_('preset'), blank=True, null=True, on_delete=models.SET_NULL)
    hdf5 = models.FileField(_('HDF5 result file'), upload_to='results/%Y/%m/%d', blank=True, max_length=1024)
    file = models.FileField(_('Output file'), upload_to='results/%Y/%m/%d', blank=True, max_length=1024)
    mime_type = models.CharField(_('Output file MIME type'), blank=True, max_length=256)
    status = models.IntegerField(_('status'), choices=STATUS, default=1)
    author = models.ForeignKey(User, related_name="results", verbose_name=_('author'), blank=True, null=True, on_delete=models.SET_NULL)

    class Meta(MetaCore):
        db_table = app + '_results'
        verbose_name = _('Result')
        verbose_name_plural = _('Results')

    def status_setter(self, status):
        self.status = status
        self.save()

    def __unicode__(self):
        return '_'.join([self.item.title, unicode(self.parameters.processor)])


class Task(BaseResource):

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
        self.status_setter(3)

        results_root = 'results'
        if not os.path.exists(settings.MEDIA_ROOT + results_root):
            os.makedirs(settings.MEDIA_ROOT + results_root)

        for item in self.selection.items.all():
            path = results_root + os.sep + item.uuid + os.sep
            if not os.path.exists(settings.MEDIA_ROOT + os.sep + path):
                os.makedirs(settings.MEDIA_ROOT + os.sep + path)

            pipe = timeside.decoder.FileDecoder(item.file.path, sha1=item.sha1)

            presets = {}
            for preset in self.experience.presets.all():
                proc = get_processor(preset.processor.pid)
                if proc.type == 'encoder':
                    result, c = Result.objects.get_or_create(preset=preset, item=item)
                    result.file = path + str(result.uuid) + '.' + proc.file_extension()
                    result.save()
                    proc = proc(result.file.path, overwrite=True)
                else:
                    proc = proc()
                #proc.set_parameters(preset.parameters)
                presets[preset] = proc
                pipe = pipe | proc

            # while item.lock:
            #     time.sleep(30)

            if not item.hdf5:
                item.hdf5 =  path + str(self.experience.uuid) + '.hdf5'
                item.save()

            pipe.run()
            item.lock_setter(True)
            pipe.results.to_hdf5(item.hdf5.path)
            item.lock_setter(False)

            for preset in presets.keys():
                proc = presets[preset]
                if proc.type == 'analyzer':
                    for processor_id in proc.results.keys():
                        parameters = proc.results[processor_id].parameters
                        preset, c = Preset.objects.get_or_create(processor=preset.processor, parameters=unicode(parameters))
                        result, c = Result.objects.get_or_create(preset=preset, item=item)
                        result.hdf5 = path + str(result.uuid) + '.hdf5'
                        proc.results.to_hdf5(result.hdf5.path)
                        result.status_setter(4)
                elif proc.type == 'grapher':
                    parameters = {}
                    result, c = Result.objects.get_or_create(preset=preset, item=item)
                    result.file = path + str(result.uuid) + '.png'
                    proc.render(output=result.file.path)
                    result.status_setter(4)
                elif proc.type == 'encoder':
                    result = Result.objects.get(preset=preset, item=item)
                    result.status_setter(4)
                del proc

            # except:
            #     self.status_setter(0)
            #     item.lock_setter(False)
            #     break

        self.status_setter(4)
        del pipe


def set_mimetype(sender, **kwargs):
    instance = kwargs['instance']
    if instance.file:
        if not instance.mime_type:
            instance.mime_type = get_mime_type(instance.file.path)

def set_hash(sender, **kwargs):
    instance = kwargs['instance']
    if instance.file:
        if not instance.sha1:
            instance.sha1 = sha1sum_file(instance.file.path)

def run(sender, **kwargs):
    instance = kwargs['instance']
    if instance.status == 2:
        instance.run()


post_save.connect(set_mimetype, sender=Item)
post_save.connect(set_hash, sender=Item)
post_save.connect(set_mimetype, sender=Result)
post_save.connect(run, sender=Task)

