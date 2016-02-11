# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Parisson SARL
# Copyright (c) 2014 Guillaume Pellerin <yomguy@parisson.com>
# Copyright (c) 2014 Thomas Fillon <thomas@parisson.com>

# This file is part of TimeSide.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Authors:
# Guillaume Pellerin <yomguy@parisson.com>
# Thomas Fillon <thomas@parisson.com>


import os
import uuid
import mimetypes

import timeside.core
from timeside.plugins.decoder.utils import sha1sum_file, sha1sum_url

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.conf import settings

app = 'timeside'

processors = timeside.core.processor.processors(timeside.core.api.IProcessor)

_processor_types = {'Analyzers': timeside.core.api.IAnalyzer,
                    'Encoders': timeside.core.api.IEncoder,
                    'Graphers': timeside.core.api.IGrapher}

PROCESSOR_PIDS = [(name, [(processor.id(), processor.id())
                          for processor
                          in timeside.core.processor.processors(proc_type)])
                  for name, proc_type in _processor_types.items()]

public_extra_types = {
    '.webm': 'video/webm',
}

encoders = timeside.core.processor.processors(timeside.core.api.IEncoder)
for encoder in encoders:
    public_extra_types['.' + encoder.file_extension()] = encoder.mime_type()

private_extra_types = {
    '.eaf': 'text/xml',  # ELAN Annotation Format
    '.trs':  'text/xml', # Trancriber Annotation Format
    '.svl':  'text/xml',  # Sonic Visualiser layer file
    '.TextGrid': 'text/praat-textgrid',  # Praat TextGrid annotation file
}

for ext,mime_type in public_extra_types.items():
    mimetypes.add_type(mime_type, ext)

for ext,mime_type in private_extra_types.items():
    mimetypes.add_type(mime_type, ext)


# Status
_FAILED, _DRAFT, _PENDING, _RUNNING, _DONE = 0, 1, 2, 3, 4
STATUS = ((_FAILED, _('failed')), (_DRAFT, _('draft')),
          (_PENDING, _('pending')), (_RUNNING, _('running')),
          (_DONE, _('done')))


results_root = 'results'
results_path = os.path.join(settings.MEDIA_ROOT, results_root)
if not os.path.exists(results_path):
    os.makedirs(results_path)


def get_mime_type(path):
    return mimetypes.guess_type(path)[0]


def get_processor(pid):
    for proc in processors:
        if proc.id() == pid:
            return proc
    raise ValueError('Processor %s does not exists' % pid)


class MetaCore:

    app_label = 'TimeSide'


class BaseResource(models.Model):

    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True,
                                         null=True)
    uuid = models.CharField(_('uuid'), unique=True, blank=True, max_length=255)

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

    items = models.ManyToManyField('Item', related_name="selections",
                                   verbose_name=_('items'), blank=True,
                                   null=True)
    selections = models.ManyToManyField('Selection',
                                        related_name="other_selections",
                                        verbose_name=_('other selections'),
                                        blank=True, null=True)
    author = models.ForeignKey(User, related_name="selections",
                               verbose_name=_('author'), blank=True, null=True,
                               on_delete=models.SET_NULL)

    class Meta(MetaCore):
        db_table = app + '_selections'
        verbose_name = _('selection')


    def get_all_items(self):
        qs_items = self.items.all()
        for selection in self.selections.all():
            qs_items |= selection.get_all_items()
        return qs_items


class Item(DocBaseResource):

    element_type = 'timeside_item'

    file = models.FileField(_('file'), upload_to='items/%Y/%m/%d',
                            blank=True, max_length=1024)
    url = models.URLField(_('URL'), blank=True, max_length=1024)
    sha1 = models.CharField(_('sha1'), blank=True, max_length=512)
    mime_type = models.CharField(_('mime type'), blank=True, max_length=256)
    hdf5 = models.FileField(_('HDF5 result file'),
                            upload_to='results/%Y/%m/%d',
                            blank=True, max_length=1024)
    author = models.ForeignKey(User, related_name="items",
                               verbose_name=_('author'), blank=True, null=True,
                               on_delete=models.SET_NULL)
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

    def get_results_path(self):
        return os.path.join(results_path, self.uuid)

    def run(self, experience):
        result_path = self.get_results_path()
        if not os.path.exists(result_path):
            os.makedirs(result_path)


        if self.file :
            uri = self.file.path
        elif self.url:
            uri = self.url

        pipe = timeside.plugins.decoder.file.FileDecoder(uri=uri,
                                                         sha1=self.sha1)
        presets = {}
        for preset in experience.presets.all():
            proc = get_processor(preset.processor.pid)
            if proc.type == 'encoder':
                result, c = Result.objects.get_or_create(preset=preset,
                                                         item=self)
                media_file = '.'.join([str(result.uuid),
                                       proc.file_extension()])
                result.file = os.path.join(result_path, media_file)
                result.save()
                proc = proc(result.file.path, overwrite=True,
                            streaming=False)
            else:
                proc = proc()
            if proc.type == 'analyzer':
                proc.set_parameters(preset.parameters)
            presets[preset] = proc
            pipe = pipe | proc

        # item.lock_setter(True)

        if not self.hdf5:
            hdf5_file = str(experience.uuid) + '.hdf5'
            self.hdf5 = os.path.join(result_path, hdf5_file)
            self.save()

        pipe.run()

        for preset, proc in presets.iteritems():
            if proc.type == 'analyzer':
                for result_id in proc.results.keys():
                    parameters = proc.results[result_id].parameters
                    preset, c = Preset.objects.get_or_create(
                        processor=preset.processor,
                        parameters=unicode(parameters))
                    result, c = Result.objects.get_or_create(preset=preset,
                                                             item=self)
                    hdf5_file = str(result.uuid) + '.hdf5'
                    result.hdf5 = os.path.join(result_path, hdf5_file)
                    # while result.lock:
                    #     time.sleep(3)
                    # result.lock_setter(True)
                    proc.results.to_hdf5(result.hdf5.path)
                    # result.lock_setter(False)
                    result.status_setter(_DONE)

            elif proc.type == 'grapher':
                parameters = {}
                result, c = Result.objects.get_or_create(preset=preset,
                                                         item=self)
                image_file = str(result.uuid) + '.png'
                result.file = os.path.join(result_path, image_file)
                proc.render(output=result.file.path)
                result.mime_type_setter(get_mime_type(result.file.path))
                result.status_setter(_DONE)

            elif proc.type == 'encoder':
                result = Result.objects.get(preset=preset, item=self)
                result.mime_type_setter(get_mime_type(result.file.path))
                result.status_setter(_DONE)

            del proc

        del pipe
        # item.lock_setter(False)


class Experience(DocBaseResource):

    presets = models.ManyToManyField('Preset', related_name="experiences",
                                     verbose_name=_('presets'), blank=True,
                                     null=True)
    experiences = models.ManyToManyField('Experience',
                                         related_name="other_experiences",
                                         verbose_name=_('other experiences'),
                                         blank=True, null=True)
    author = models.ForeignKey(User, related_name="experiences",
                               verbose_name=_('author'), blank=True, null=True,
                               on_delete=models.SET_NULL)
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
            self.version = timeside.core.__version__
        super(Processor, self).save(**kwargs)


class Preset(BaseResource):

    processor = models.ForeignKey('Processor', related_name="presets",
                                  verbose_name=_('processor'), blank=True,
                                  null=True)
    parameters = models.TextField(_('Parameters'), blank=True, default='{}')
    author = models.ForeignKey(User, related_name="presets",
                               verbose_name=_('author'), blank=True, null=True,
                               on_delete=models.SET_NULL)
    is_public = models.BooleanField(default=False)

    class Meta(MetaCore):
        db_table = app + '_presets'
        verbose_name = _('Preset')
        verbose_name_plural = _('Presets')

    def __unicode__(self):
        return '_'.join([unicode(self.processor), str(self.id)])


class Result(BaseResource):

    item = models.ForeignKey('Item', related_name="results",
                             verbose_name=_('item'), blank=True, null=True,
                             on_delete=models.SET_NULL)
    preset = models.ForeignKey('Preset', related_name="results",
                               verbose_name=_('preset'), blank=True, null=True,
                               on_delete=models.SET_NULL)
    hdf5 = models.FileField(_('HDF5 result file'),
                            upload_to='results/%Y/%m/%d', blank=True,
                            max_length=1024)
    file = models.FileField(_('Output file'), upload_to='results/%Y/%m/%d',
                            blank=True, max_length=1024)
    mime_type = models.CharField(_('Output file MIME type'), blank=True,
                                 max_length=256)
    status = models.IntegerField(_('status'), choices=STATUS, default=_DRAFT)
    author = models.ForeignKey(User, related_name="results",
                               verbose_name=_('author'), blank=True, null=True,
                               on_delete=models.SET_NULL)
    # lock = models.BooleanField(default=False)

    class Meta(MetaCore):
        db_table = app + '_results'
        verbose_name = _('Result')
        verbose_name_plural = _('Results')

    def status_setter(self, status):
        self.status = status
        self.save()

    def mime_type_setter(self, mime_type):
        self.mime_type = mime_type
        self.save()

    def lock_setter(self, lock):
        self.lock = lock
        self.save()

    def __unicode__(self):
        return '_'.join([self.item.title, unicode(self.preset.processor)])


class Task(BaseResource):

    experience = models.ForeignKey('Experience', related_name="task",
                                   verbose_name=_('experience'), blank=True,
                                   null=True)
    selection = models.ForeignKey('Selection', related_name="task",
                                  verbose_name=_('selection'), blank=True,
                                  null=True)
    status = models.IntegerField(_('status'), choices=STATUS, default=_DRAFT)
    author = models.ForeignKey(User, related_name="tasks",
                               verbose_name=_('author'), blank=True, null=True,
                               on_delete=models.SET_NULL)

    class Meta(MetaCore):
        db_table = app + '_tasks'
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

    def __unicode__(self):
        return '_'.join([unicode(self.selection), unicode(self.experience), unicode(self.id)])

    def status_setter(self, status):
        self.status = status
        self.save()

    def run(self, streaming=False):
        from timeside.server.tasks import experience_run
        self.status_setter(_RUNNING)
        for item in self.selection.get_all_items():
            experience_run.delay(self.experience.id, item.id)
        self.status_setter(_DONE)


def set_mimetype(sender, **kwargs):
    instance = kwargs['instance']
    if instance.file:
        path = instance.file.path
    elif (sender == Item):
        if instance.url:
            path = instance.url
    else:
        return
    mime_type = get_mime_type(path)
    if instance.mime_type == mime_type:
        return
    else:
        instance.mime_type = get_mime_type(path)
        super(sender, instance).save()

def set_hash(sender, **kwargs):
    instance = kwargs['instance']
    if instance.file:
        sha1 = sha1sum_file(instance.file.path)
    elif instance.url:
        sha1 = sha1sum_url(instance.url)
    else:
        return
    if instance.sha1 == sha1:
        return
    else:
        instance.sha1 = sha1
        super(sender, instance).save()


def run(sender, **kwargs):
    from timeside.server.tasks import task_run
    instance = kwargs['instance']
    if instance.status == _PENDING:
        task_run.delay(instance.id)


post_save.connect(set_mimetype, sender=Item)
post_save.connect(set_hash, sender=Item)
post_save.connect(set_mimetype, sender=Result)
post_save.connect(run, sender=Task)
