# -*- coding: utf-8 -*-
#
# Copyright (c) 2014-2016 Parisson SARL
# Copyright (c) 2014-2016 Guillaume Pellerin <yomguy@parisson.com>
# Copyright (c) 2014-2016 Thomas Fillon <thomas@parisson.com>

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


from __future__ import unicode_literals
import os
import uuid
import mimetypes
import ast
import time
import datetime
import gc
from shutil import copyfile
from builtins import str
from urllib.parse import urlparse
from functools import wraps

import timeside.core
from timeside.plugins.decoder.utils import sha1sum_file, sha1sum_url
from timeside.core.tools.parameters import DEFAULT_SCHEMA
from timeside.core.exceptions import ProviderError

from django.db import models, transaction
from django.utils.functional import lazy
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import (
    post_save,
    pre_save,
    pre_delete,
)
from django.conf import settings
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core.files import File
from celery.utils.log import get_task_logger

import jsonfield
import json
from requests import get

from inspect import cleandoc

# XMLtoJSON
from xml.etree.ElementTree import fromstring
from xmljson import abdera as ab

import logging

import redis

r = redis.Redis.from_url(settings.MESSAGE_BROKER)


worker_logger = get_task_logger(__name__)
app = 'timeside'
app_logger = logging.getLogger(app)

processors = timeside.core.processor.processors(timeside.core.api.IProcessor)
# providers = timeside.core.provider.providers(timeside.core.api.IProvider)


_processor_types = {'Analyzers': timeside.core.api.IAnalyzer,
                    'Encoders': timeside.core.api.IEncoder,
                    'Graphers': timeside.core.api.IGrapher}


def get_processor_pids():
    return [(name, [(processor.id(), processor.id())
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
    '.trs': 'text/xml',  # Trancriber Annotation Format
    '.svl': 'text/xml',  # Sonic Visualiser layer file
    '.TextGrid': 'text/praat-textgrid',  # Praat TextGrid annotation file
    '.h5': 'application/x-hdf5',    # HDF5
    '.hdf5': 'application/x-hdf5',  # HDF5
}

for ext, mime_type in public_extra_types.items():
    if not mimetypes.guess_extension(mime_type) == ext:
        mimetypes.add_type(mime_type, ext)

for ext, mime_type in private_extra_types.items():
    mimetypes.add_type(mime_type, ext)


# Tasks and Results status
_FAILED, _DRAFT, _PENDING, _RUNNING, _DONE = 0, 1, 2, 3, 4

STATUS = ((_FAILED, _('failed')),
          (_DRAFT, _('draft')),
          (_PENDING, _('pending')),
          (_RUNNING, _('running')),
          (_DONE, _('done')))

# Analysis render type
_VECTOR, _IMAGE, _LIST = 0, 1, 2

RENDER_TYPES = ((_VECTOR, _('vector')),
                (_IMAGE, _('image')),
                )


def prevent_recursion(func):
    @wraps(func)
    def no_recursion(sender, instance=None, **kwargs):
        if not instance:
            return
        if hasattr(instance, '_dirty'):
            return

        func(sender, instance=instance, **kwargs)

        try:
            instance._dirty = True
            instance.save()
        finally:
            del instance._dirty

    return no_recursion


def on_transaction_commit(func):
    def inner(*args, **kwargs):
        transaction.on_commit(lambda: func(*args, **kwargs))
    return inner


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


def get_mime_type(path):
    return mimetypes.guess_type(path)[0]

# make every user having an automatically generated Token
# catching the User's post_save signal
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# --- Abstract classes -----
class Dated(models.Model):

    date_added = models.DateTimeField(
        _('date added'),
        auto_now_add=True,
        null=True
        )
    date_modified = models.DateTimeField(
        _('date modified'),
        auto_now=True,
        null=True
        )

    class Meta:
        abstract = True


class UUID(models.Model):

    uuid = models.UUIDField(
        _('uuid'),
        default=uuid.uuid4,
        primary_key=True,
        blank=False,
        max_length=255,
        editable=False,
        unique=True
        )

    class Meta:
        abstract = True

    @classmethod
    def get_first_or_create(cls, **kwargs):
        """
        duplicates-compatible get or create method
        """
        objs = cls.objects.filter(**kwargs)
        if objs:
            obj = objs[0]
            created = False
        else:
            obj = cls(**kwargs)
            obj.save()
            created = True
        return obj, created


    @classmethod
    def get_first(cls, **kwargs):
        """
         get first object
        """
        objs = cls.objects.filter(**kwargs)
        return objs[0]


class Titled(models.Model):

    title = models.CharField(_('title'), blank=True, max_length=512)
    description = models.TextField(_('description'), blank=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class Named(models.Model):

    name = models.CharField(_('name'), blank=True, max_length=512)
    description = models.TextField(_('description'), blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        abstract = True


class Shareable(models.Model):

    author = models.ForeignKey(
        User,
        related_name="%(class)s",
        verbose_name=_('author'),
        blank=True, null=True,
        on_delete=models.SET_NULL
        )
    is_public = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Provider(Named, UUID):

    pid = models.CharField(_('pid'), blank=True, max_length=128)
    domain = models.CharField(_('domain'), blank=True, max_length=1024)
    source_access = models.BooleanField(
        help_text=_(
            "Whether or not the audio is "
            "freely available from the provider."
            ),
        default=False,
        )

    def __str__(self):
        return str(self.pid)

    def get_resource(self, url=None, id=None,
                        download=False, path=settings.DOWNLOAD_ROOT):
        provider = timeside.core.provider.get_provider(self.pid)
        self.resource = provider(url=url,
                            id=id,
                            path=settings.DOWNLOAD_ROOT,
                            download=download
                            )
        return self.resource

    def get_title(self):
        return self.resource.get_title()

    def get_file(self):
        return self.resource.get_file()


class Selection(Titled, UUID, Dated, Shareable):

    items = models.ManyToManyField(
        'Item',
        related_name="selections",
        verbose_name=_('items'),
        blank=True
        )
    selections = models.ManyToManyField(
        'Selection',
        related_name="other_selections",
        verbose_name=_('other selections'),
        blank=True,
        help_text=_("Include other selections in an selection."))

    class Meta:
        verbose_name = _('selection')
        ordering = ['-date_modified']

    def get_all_items(self):
        qs_items = self.items.all()
        for selection in self.selections.all():
            qs_items |= selection.get_all_items()
        return qs_items


class Item(Titled, UUID, Dated, Shareable):
    """Object representing an audio content
    """

    element_type = 'timeside_item'

    album = models.CharField(
        _('album'), blank=True, max_length=256
        )
    artist = models.CharField(
        _('artist'), blank=True, max_length=256
        )
    source_file = models.FileField(
        _('source file'),
        upload_to='items/%Y/%m/%d',
        blank=True,
        max_length=1024,
        help_text=_("Audio source file to process")
        )
    source_url = models.URLField(
        _('source URL'),
        blank=True,
        max_length=1024,
        help_text=_("Audio source streamable URL to process")
        )
    audio_duration = models.FloatField(
        _('duration'), blank=True, null=True,
        help_text=_("Duration of the audio source")
        )
    samplerate = models.IntegerField(
        _('sampling rate'), blank=True, null=True,
        help_text=_("Sampling rate of audio source")
    )
    sha1 = models.CharField(
        _('sha1'), blank=True, max_length=512
        )
    mime_type = models.CharField(
        _('mime type'), blank=True, max_length=256
        )
    provider = models.ForeignKey(
        'Provider',
        verbose_name=_('provider'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_("Audio provider (e.g. Deezer, Youtube, etc.)")
        )
    external_id = models.CharField(
        _('external ID'), blank=True, max_length=256,
        help_text=_(cleandoc("""
            Provider's id of the audio source.\n
            e.g. for Deezer preview: 4763165\n
            e.g. for YouTube: oRdxUFDoQe0
            """))
        )
    external_uri = models.CharField(
        _('external URI'), blank=True, max_length=1024,
        help_text=_(cleandoc("""
        Provider's URI of the audio source.\n
        e.g. for Deezer preview: http://www.deezer.com/track/4763165\n
        e.g. for YouTube: https://www.youtube.com/watch?v=oRdxUFDoQe0
        """))
        )
    picture_url = models.URLField(
        _('picture URL'), blank=True, max_length=1024,
        )
    lock = models.BooleanField(default=False)
    test = models.BooleanField(
        default=False,
        help_text=_('testing purpose')
        )

    class Meta:
        ordering = ['-date_modified']
        verbose_name = _('item')

    def __str__(self):
        text = ''
        if self.title:
            text = ' - '.join([str(self.title), str(self.uuid)[:8]])
        else:
            text = str(self.uuid)
        if self.mime_type:
            text += ' - ' + self.mime_type
        return text

    def results(self):
        return [result for result in self.results.all()]

    def lock_setter(self, lock):
        self.lock = lock
        self.save()

    def get_resource(self, download=False):
        """
        Return item title and source_file from provider
        """
        title = ""
        source_file = ""

        if self.provider and self.provider.source_access:
            try:
                self.resource = self.provider.get_resource(
                        url=self.external_uri,
                        id=self.external_id,
                        download=download
                        )
                title = self.resource.get_title()
                source_file = self.resource.get_file()
            except timeside.core.exceptions.ProviderError as e:
                app_logger.warning(e)
                self.external_uri = ''
                self.external_id = ''

        return title, source_file

    def get_external_id(self):
        """
        Return item resource ID
        """
        return self.external_id

    def get_uri(self):
        """
        Return the Item source URI
        """

        if self.source_file and os.path.exists(self.source_file.path):
            return self.source_file.path
        elif self.source_url:
            return self.source_url
        return None

    def get_results_path(self):
        """
        Return Item result path
        """

        return os.path.join(settings.RESULTS_ROOT, str(self.uuid))

    def get_audio_duration(self, force=False):
        """
        Return item audio duration
        """

        audio_duration = None
        if (
            (force or not self.audio_duration)
            and self.source_file
           ):
            decoder = timeside.core.get_processor(settings.TIMESIDE_DEFAULT_DECODER)(
                uri=self.get_uri())
            return decoder.uri_duration
        else:
            return self.audio_duration

    def get_audio_samplerate(self, force=False):
        """
        Return item audio samplerate
        """

        samplerate = None
        if (
            (force or not self.samplerate)
            and self.source_file
           ):
            decoder = timeside.core.get_processor(settings.TIMESIDE_DEFAULT_DECODER)(
                uri=self.get_uri())
            return decoder.input_samplerate
        else:
            return self.samplerate

    def get_hash(self, force=False):
        """
        Set SHA1 hash from file binary content
        """

        sha1 = ''
        if force or not self.sha1:
            if self.source_file:
                sha1 = sha1sum_file(self.source_file.path)
            elif self.source_url:
                sha1 = sha1sum_url(self.source_url)
        return sha1

    def get_mime_type(self, force=False):
        """
        """

        mime_type = ''
        if force or not self.mime_type:
            if self.source_url:
                path = self.source_url
            elif self.source_file:
                path = self.source_file.path
            if os.path.exists(path):
                mime_type = get_mime_type(path)
        return mime_type

    def process_waveform(self):
        processor = Processor.get_first(pid='waveform_analyzer')
        preset, c = Preset.get_first_or_create(processor=processor)
        experience = preset.get_single_experience()
        task, c = Task.get_first_or_create(item=self, experience=experience)
        if c or task.status != _DONE:
            task.run()

    def get_provider(self):
        domain = urlparse(self.external_uri).netloc
        providers = Provider.objects.filter(domain=domain)
        if providers:
            self.provider = providers[0]

    def get_audio_metadata(self):
        self.sha1 = self.get_hash()
        self.mime_type = self.get_mime_type()
        self.audio_duration = self.get_audio_duration()
        self.samplerate = self.get_audio_samplerate()
        self.process_waveform()

    def save_without_signals(self):
        """
        This allows for updating the model from code running inside post_save()
        signals without going into an infinite loop:
        """
        self._disable_signals = True
        self.save()
        self._disable_signals = False


@receiver(post_save, sender=Item)
@on_transaction_commit
def item_post_save(sender, **kwargs):
    from timeside.server.tasks import item_post_save_async3
    instance = kwargs['instance']
    if not getattr(instance, '_disable_signals', False):
        item_post_save_async3.delay(uuid=instance.uuid)


class Experience(Titled, UUID, Dated, Shareable):

    presets = models.ManyToManyField(
        'Preset',
        related_name="experiences",
        verbose_name=_('presets'),
        blank=True
        )
    experiences = models.ManyToManyField(
        'Experience',
        related_name="other_experiences",
        verbose_name=_('other experiences'),
        blank=True,
        help_text=_("Include other experiences in an experience.")
        )

    class Meta:
        verbose_name = _('Experience')
        ordering = ['-date_modified']

    def __str__(self):
        if self.title:
            return self.title
        elif self.presets:
            return str(self.presets.all()[0]) + "..."

    def run(self, task=None, item=None):
        if task and item:
            task_uuid = str(task.uuid)
            experience_uuid = str(self.uuid)
            item_uuid = str(item)

            def progress_callback(completion):
                r.publish(
                    'timeside-experience-progress',
                    'timeside' +
                    ":" + task_uuid +
                    ":" + experience_uuid +
                    ":" + item_uuid +
                    ":" + str(completion)
                    )
        else:
            progress_callback = None

        if item:
            result_path = item.get_results_path()
            uri = item.get_uri()
            decoder = timeside.core.get_processor('aubio_decoder')(
                uri=uri,
                sha1=item.sha1,
                progress_callback=progress_callback
                )
        else:
            result_path = settings.RESULTS_ROOT
            decoder = timeside.core.get_processor('null_decoder')()

        pipe = decoder

        parent_analyzers = []
        # search for parent analyzer presets
        # not to add as duplicates in the pipe
        for preset in self.presets.all():
            proc = preset.processor.get_processor()
            if proc.type in ['analyzer', 'grapher']:
                try:
                    proc = proc(parameters=preset.parameters)
                except:
                    proc = proc(**preset.parameters)
                if 'analyzer' in proc.parents:
                    parent_analyzers.append(proc.parents['analyzer'])

        presets = {}
        for preset in self.presets.all():
            # get core audio metaProcessor
            # corresponding to preset.processor.pid
            proc = preset.processor.get_processor()
            if proc.type == 'encoder':
                result, c = Result.objects.get_or_create(preset=preset,
                                                         item=item)
                media_file = '.'.join([str(result.uuid),
                                       proc.file_extension()])
                result.file = os.path.join(result_path, media_file).replace(
                    settings.MEDIA_ROOT, ''
                    )
                result.save()
                # instantiate a core processor of an encoder
                proc = proc(result.file.path, overwrite=True,
                            streaming=False)
                worker_logger.info(f'Run {str(proc)} on {str(item)}')
            elif proc.type in ['analyzer', 'grapher']:
                # instantiate a core processor of an analyzer or a grapher
                try:
                    proc = proc(parameters=preset.parameters)
                except:
                    proc = proc(**preset.parameters)
                worker_logger.info(
                    f'Run {proc} on {item} with {preset.parameters}'
                    )

            if proc not in parent_analyzers:
                presets[preset] = proc
                pipe |= proc

        pipe.run()

        def set_results_from_processor(proc, preset=None):
            if preset:
                parameters = preset.parameters
            elif preset is None:
                processor, c = Processor.get_first_or_create(pid=proc.id())
                parameters = json.dumps(processor.get_parameters_default())
                preset, c = Preset.get_first_or_create(
                    processor=processor,
                    parameters=parameters
                    )

            result, c = Result.get_first_or_create(
                preset=preset,
                item=item
                )

            if not hasattr(proc, 'external'):
                if not proc.results.export_mode or proc.results.export_mode == "hdf5":
                    export_file = str(result.uuid) + '.hdf5'
                    result.hdf5 = os.path.join(
                        result_path,
                        export_file
                        ).replace(settings.MEDIA_ROOT, '')
                    proc.results.to_hdf5(result.hdf5.path)
                elif proc.results.export_mode == "json":
                    export_file = str(result.uuid) + '.json'
                    result.file = os.path.join(
                        result_path,
                        export_file
                        ).replace(settings.MEDIA_ROOT, '')
                    proc.results.to_json(result.file.path)
                elif proc.results.export_mode == "xml":
                    export_file = str(result.uuid) + '.xml'
                    result.file = os.path.join(
                        result_path,
                        export_file
                        ).replace(settings.MEDIA_ROOT, '')
                    proc.results.to_xml(result.file.path)
            else:
                if proc.external:
                    filename = proc.result_temp_file.split(os.sep)[-1]
                    name, ext = filename.split('.')
                    filename = str(result.uuid) + '.' + ext
                    result_file = os.path.join(result_path, filename)
                    copyfile(proc.result_temp_file, result_file)
                    if ext == 'xml':
                        # XML to JSON conversion
                        filename_json = str(result.uuid) + '.' + 'json'
                        result_file = os.path.join(result_path, filename_json)
                        f_xml = open(proc.result_temp_file, 'r')
                        xml = f_xml.read()
                        f = open(result_file, 'w+')
                        f.write(json.dumps(ab.data(fromstring(xml)), indent=4))
                        f.close()
                        f_xml.close()
                    result.file = result_file.replace(settings.MEDIA_ROOT, '')

            result.run_time_setter(proc.run_time)
            result.status_setter(_DONE)

        for preset, proc in presets.items():
            if proc.type == 'analyzer':
                # TODO : set_proc_results
                set_results_from_processor(proc, preset)

            elif proc.type == 'grapher':
                result, c = Result.objects.get_or_create(preset=preset,
                                                         item=item)
                image_file = str(result.uuid) + '.png'
                start = datetime.datetime.utcnow()
                result.file = os.path.join(
                    result_path,
                    image_file
                    ).replace(settings.MEDIA_ROOT, '')

                # TODO : set as an option
                proc.watermark('timeside', opacity=.6, margin=(5, 5))
                proc.render(output=result.file.path)
                run_time = datetime.datetime.utcnow() - start
                result.run_time_setter(run_time)
                result.mime_type_setter(get_mime_type(result.file.path))
                result.status_setter(_DONE)

                if 'analyzer' in proc.parents:
                    analyzer = proc.parents['analyzer']
                    set_results_from_processor(analyzer, None)

            elif proc.type == 'encoder':
                result = Result.objects.get(preset=preset, item=item)
                result.run_time_setter(proc.run_time)
                result.mime_type_setter(get_mime_type(result.file.path))
                result.status_setter(_DONE)

            if hasattr(proc, 'values'):
                proc.values = None
                del proc.values
            if hasattr(proc, 'result'):
                proc.result = None
                del proc.result
            if hasattr(proc, 'results'):
                try:
                    proc.results = None
                    del proc.results
                except:  # noqa
                    continue
            del proc

        del pipe
        gc.collect()


class Processor(Named, UUID):

    pid = models.CharField(_('pid'), max_length=128)
    version = models.CharField(_('version'), max_length=64, blank=True)
    synchronous = models.BooleanField(
        default=False,
        help_text=_('executed in main thread synchronously')
        )

    def __init__(self, *args, **kwargs):
        super(Processor, self).__init__(*args, **kwargs)
        self._meta.get_field('pid')._choices = lazy(get_processor_pids, list)()

    class Meta:
        verbose_name = _('processor')
        ordering = ['pid', '-version']

    def __str__(self):
        return self.pid + '-v' + self.version

    def save(self, **kwargs):
        if not self.version:
            try:
                self.version = self.get_processor().version()
            except AttributeError:
                pass
        if not self.name:
            try:
                self.name = self.get_processor().name()
            except AttributeError:
                pass
        super(Processor, self).save(**kwargs)

    def get_processor(self):
        return timeside.core.get_processor(self.pid)

    def get_parameters_schema(self):
        try:
            proc = self.get_processor()
        except:
            proc = None

        if proc:
            return proc.get_parameters_schema()
        else:
            return None

    def get_parameters_default(self):
        try:
            proc = self.get_processor()
        except:
            proc = None

        if proc:
            return proc.get_parameters_default()
        else:
            return None


class SubProcessor(UUID):
    """Store a result id associated with a given Processor"""
    sub_processor_id = models.CharField(_('sub_processor_id'), max_length=128)
    name = models.CharField(_('name'), max_length=256, blank=True)
    processor = models.ForeignKey(
        'Processor',
        related_name="sub_results",
        verbose_name=_('processor'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL
        )

    class Meta:
        verbose_name = _('Subprocessor')
        ordering = ['sub_processor_id',]

    def __str__(self):
        return self.sub_processor_id


class Preset(UUID, Dated, Shareable):

    processor = models.ForeignKey(
        'Processor',
        related_name="presets",
        verbose_name=_('processor'),
        blank=True, null=True,
        on_delete=models.SET_NULL
        )
    parameters = models.JSONField(_('Parameters'), blank=True, default=dict)

    class Meta:
        verbose_name = _('Preset')
        verbose_name_plural = _('Presets')
        ordering = ['-date_modified', 'processor__pid',]

    def __str__(self):
        return str(self.processor) + '_' + str(self.uuid)[:4]

    def get_single_experience(self):
        exp_title = "Simple experience for preset %s" % self.__str__()
        exp_description = "\n".join(
            [
                exp_title,
                "Automatically generated by the TimeSide application."
            ])
        experience, created = Experience.objects.get_or_create(
            title=exp_title,
            description=exp_description
            )
        if created:
            experience.save()
            experience.presets.add(self)
        elif (experience.presets.count() > 1) or (self not in experience.presets.all()):  # noqa
            experience.presets.clear()
            experience.presets.add(self)

        return experience


class Result(UUID, Dated, Shareable):

    item = models.ForeignKey(
        'Item',
        related_name="results",
        verbose_name=_('item'),
        blank=True, null=True,
        on_delete=models.SET_NULL,
        help_text=_("Item on which a preset has been applied.")
        )
    preset = models.ForeignKey(
        'Preset',
        related_name="results",
        verbose_name=_('preset'),
        blank=True, null=True,
        on_delete=models.SET_NULL,
        help_text=_("Preset applied on an item.")
        )
    hdf5 = models.FileField(
        _('HDF5 result file'),
        upload_to='results/%Y/%m/%d',
        blank=True,
        max_length=1024,
        help_text=_(
            "Numerical result of the processing stored in an hdf5 file."
            )
        )
    file = models.FileField(
        _('Output file'),
        upload_to='results/%Y/%m/%d',
        blank=True,
        max_length=1024,
        help_text=_(cleandoc("""
            Non numerical result stored in a file
            (image, transcoded audio, etc.)
            """))
        )
    mime_type = models.CharField(
        _('Output file MIME type'),
        blank=True,
        max_length=256
        )
    status = models.IntegerField(
        _('status'),
        choices=STATUS,
        default=_DRAFT,
        help_text=_(cleandoc(f"""
                Status of the task giving the result:\n
                failed: {_FAILED}\n
                draft: {_DRAFT}\n
                pending: {_PENDING}\n
                running: {_RUNNING}\n
                done: {_DONE}
                """))
        )
    run_time = models.DurationField(
        _('Run time'),
        blank=True,
        null=True,
        help_text=_("Duration of the result computing.")
        )
    # lock = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Result')
        verbose_name_plural = _('Results')
        ordering = ['-date_modified']

    def status_setter(self, status):
        self.status = status
        self.save()

    def mime_type_setter(self, mime_type):
        self.mime_type = mime_type
        self.save()

    def lock_setter(self, lock):
        self.lock = lock
        self.save()

    def has_file(self):
        return bool(self.file and os.path.exists(self.file.path))

    def has_hdf5(self):
        return bool(self.hdf5 and os.path.exists(self.hdf5.path))

    def run_time_setter(self, run_time):
        self.run_time = run_time
        self.save()

    def get_mimetype(self, force=False):
        if force or (self.mime_type is None):
            mime_type = get_mime_type(self.file.path)
            self.mime_type_setter(mime_type=mime_type)

    def __str__(self):
        if self.preset:
            if self.item:
                return self.item.title + '_' + str(self.preset)
            else:
                return str(self.preset)
        else:
            return 'Unnamed_result'


def result_pre_delete(sender, **kwargs):
    """ """
    instance = kwargs['instance']
    if instance.file and os.path.exists(instance.file.path):
        os.remove(instance.file.path)
    if instance.hdf5 and os.path.exists(instance.hdf5.path):
        os.remove(instance.hdf5.path)


pre_delete.connect(result_pre_delete, sender=Result)
# TODO post_save.connect(set_mimetype, sender=Result)


class Task(UUID, Dated, Shareable):

    experience = models.ForeignKey(
        'Experience',
        related_name="task",
        verbose_name=_('experience'),
        blank=True, null=True,
        on_delete=models.SET_NULL,
        help_text=_("Experience prossessed in the task.")
        )
    selection = models.ForeignKey(
        'Selection',
        related_name="task",
        verbose_name=_('selection'),
        blank=True, null=True,
        on_delete=models.SET_NULL,
        help_text=_("Selection prossessed in the task.")
        )
    item = models.ForeignKey(
        'Item',
        related_name="task",
        verbose_name=_('item'),
        blank=True, null=True,
        on_delete=models.SET_NULL,
        help_text=_("Single item prossessed in the task.")
        )

    status = models.IntegerField(
        _('status'),
        choices=STATUS,
        default=_PENDING,
        blank=True, null=True,
        help_text=_(cleandoc(f"""
            Task's status:\n
            failed: {_FAILED}\n
            draft: {_DRAFT}\n
            pending: {_PENDING}\n
            running: {_RUNNING}\n
            done: {_DONE}
            """))
        )

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
        ordering = ['-date_modified']

    def __str__(self):
        if self.item:
            return '_'.join(
                [str(self.item), str(self.experience), str(self.uuid)[:4]]
                )
        elif self.selection:
            return '_'.join(
                [str(self.selection), str(self.experience), str(self.uuid)[:4]]
                )
        else:
            return '_'.join(
                [str(self.experience), str(self.uuid)[:4]]
                )

    def save(self, **kwargs):
        if not self.status:
            self.status = _PENDING
        super(Task, self).save(**kwargs)

    def status_setter(self, status):
        self.status = status
        self.save()

    def is_done(self):
        return (self.status == _DONE)

    def run_experience(self, item_uuid):
        from .tasks import experience_run

        if self.synchronous:
            self.results.append(
                experience_run(
                    task_id=str(self.uuid),
                    experience_id=str(self.experience.uuid),
                    item_id=item_uuid,
                )
            )
        else:
            self.results.append(
                experience_run.delay(
                    task_id=str(self.uuid),
                    experience_id=str(self.experience.uuid),
                    item_id=item_uuid,
                )
            )
            self.results_ids = [res.id for res in self.results]

    def run(self, streaming=False):
        from .tasks import task_monitor

        self.status_setter(_RUNNING)
        self.results = []
        self.results_ids = []

        self.synchronous = False
        for preset in self.experience.presets.all():
            if preset.processor.synchronous:
                self.synchronous = True

        if self.selection:
            for item in self.selection.get_all_items():
                self.run_experience(str(self.item.uuid))
        elif self.item:
            self.run_experience(str(self.item.uuid))
        elif not self.item:
            self.run_experience(None)

        if self.synchronous:
            task_monitor(self.uuid, self.results_ids)
        else:
            task_monitor.delay(self.uuid, self.results_ids)


def task_run_now(sender, **kwargs):
    task = kwargs['instance']
    if task.status == _PENDING:
        task.run()

post_save.connect(task_run_now, sender=Task)



# Session and Tracks related objects

class Analysis(Titled, UUID, Dated, Shareable):
    sub_processor = models.ForeignKey(
        SubProcessor,
        related_name="analysis",
        verbose_name=_('sub_processor'),
        blank=False,
        on_delete=models.CASCADE
        )
    preset = models.ForeignKey(
        Preset,
        related_name="analysis",
        verbose_name=_('preset'),
        blank=False,
        on_delete=models.CASCADE
        )
    render_type = models.IntegerField(
        _('render type'),
        choices=RENDER_TYPES,
        default=_VECTOR,
        help_text=_(cleandoc(f"""
            Rendering types:\n
            vector: {_VECTOR}\n
            image: {_IMAGE}\n
            """))
        )
    featured = models.BooleanField(default=False)
    parameters_schema = models.JSONField(default=dict)

    class Meta:
        verbose_name = _('Analysis')
        verbose_name_plural = _('Analyses')
        ordering = ['-date_modified', 'title']

    def save(self, **kwargs):
        if self.sub_processor:
            print(self.sub_processor)
            self.parameters_schema = self.sub_processor.processor.get_parameters_schema()
        super(Analysis, self).save(**kwargs)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return str(self.preset)


class AnalysisTrack(Titled, UUID, Dated, Shareable):

    analysis = models.ForeignKey(
        Analysis,
        related_name='tracks',
        verbose_name=_('analysis'),
        blank=False,
        on_delete=models.CASCADE
        )
    item = models.ForeignKey(
        Item,
        related_name='analysis_tracks',
        verbose_name=_('item'),
        blank=True,
        null=True,
        on_delete=models.CASCADE
        )
    color = models.CharField(
        _('RVB color'),
        max_length=6,
        blank=True
        )

    class Meta:
        verbose_name = _('Analysis Track')
        ordering = ['-date_modified']

    def __str__(self):
        if self.item:
            return self.analysis.title + ' - ' + self.item.title
        else:
            return self.analysis.title


class AnnotationTrack(Titled, UUID, Dated, Shareable):

    item = models.ForeignKey(
        Item,
        related_name='annotation_tracks',
        verbose_name=_('item'),
        blank=False,
        on_delete=models.CASCADE
        )
    start_time = models.FloatField(_('start time (s)'), default=0)
    overlapping = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Annotation Track')
        ordering = ['-date_modified']


class Annotation(Titled, UUID, Dated, Shareable):

    track = models.ForeignKey(
        AnnotationTrack, related_name='annotations',
        verbose_name=_('annotation'),
        blank=False,
        on_delete=models.CASCADE
        )
    
    results = models.ManyToManyField(
        'Result',
        related_name="annotations",
        verbose_name=_('results'),
        blank=True
        )

    start_time = models.FloatField(_('start time (s)'), default=0)
    stop_time = models.FloatField(_('stop time (s)'))

    class Meta:
        verbose_name = _('Annotation')
        ordering = ['-date_modified']
