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

import timeside.core
from timeside.plugins.decoder.utils import sha1sum_file, sha1sum_url
from timeside.core.tools.parameters import DEFAULT_SCHEMA
from django.db import models
from django.utils.functional import lazy
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
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
import youtube_dl
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
STATUS = ((_FAILED, _('failed')), (_DRAFT, _('draft')),
          (_PENDING, _('pending')), (_RUNNING, _('running')),
          (_DONE, _('done')))

# Analysis render type
_VECTOR, _IMAGE,  = 0, 1
RENDER_TYPES = ((_VECTOR, _('vector')), (_IMAGE, _('image')))

RESULTS_ROOT = os.path.join(settings.MEDIA_ROOT, 'results')
if not os.path.exists(RESULTS_ROOT):
    os.makedirs(RESULTS_ROOT)

DOWNLOAD_ROOT = os.path.join(
            settings.MEDIA_ROOT, 'items', 'download', ''
            )
if not os.path.exists(DOWNLOAD_ROOT):
    os.makedirs(DOWNLOAD_ROOT)


DEFAULT_DECODER = getattr(settings, 'TIMESIDE_DEFAULT_DECODER', 'aubio_decoder')


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


@python_2_unicode_compatible
class Titled(models.Model):

    title = models.CharField(_('title'), blank=True, max_length=512)
    description = models.TextField(_('description'), blank=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


@python_2_unicode_compatible
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


@python_2_unicode_compatible
class Provider(Named, UUID):

    pid = models.CharField(_('pid'), blank=True, max_length=128)
    source_access = models.BooleanField(
        help_text=_(
            "Whether or not the audio is "
            "freely available from the provider."
            ),
        default=False,
        )

    def __str__(self):
        return str(self.pid)

    def get_provider(self, url=None, id=None, download=False):
        provider = timeside.core.provider.get_provider(self.pid)
        self.provider = provider(url=url,
                            id=id,
                            path=DOWNLOAD_ROOT,
                            download=download
                            )
        return self.provider

    def get_source(self):
        return self.provider.get_source()

    def get_id_from_url(self, url):
        return self.provider.get_id_from_url()


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


@python_2_unicode_compatible
class Item(Titled, UUID, Dated, Shareable):

    element_type = 'timeside_item'

    source_file = models.FileField(
        _('file'), upload_to='items/%Y/%m/%d', blank=True, max_length=1024,
        help_text=_("Audio file to process.")
        )
    source_url = models.URLField(
        _('URL'), blank=True, max_length=1024,
        help_text=_("URL of a streamable audio source to process.")
        )
    audio_duration = models.FloatField(
        _('duration'), blank=True, null=True,
        help_text=_("Duration of audio track.")
        )
    samplerate = models.IntegerField(
        _('sampling rate'), blank=True, null=True,
        help_text=_("Sampling rate of audio source file.")
    )
    sha1 = models.CharField(
        _('sha1'), blank=True, max_length=512
        )
    mime_type = models.CharField(
        _('mime type'), blank=True, max_length=256
        )
    hdf5 = models.FileField(
        _('HDF5 result file'),
        upload_to='results/%Y/%m/%d',
        blank=True,
        max_length=1024,
        )
    lock = models.BooleanField(default=False)
    external_uri = models.CharField(
        _('external_uri'), blank=True, max_length=1024,
        help_text=_(cleandoc("""
        Provider's URI of the audio source.\n
        e.g. for Deezer preview: http://www.deezer.com/track/4763165\n
        e.g. for YouTube: https://www.youtube.com/watch?v=oRdxUFDoQe0
        """))
        )
    external_id = models.CharField(
        _('external_id'), blank=True, max_length=256,
        help_text=_(cleandoc("""
            Provider's id of the audio source.\n
            e.g. for Deezer preview: 4763165\n
            e.g. for YouTube: oRdxUFDoQe0
            """))
        )
    provider = models.ForeignKey(
        'Provider',
        verbose_name=_('provider'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_("Audio provider (e.g. Deezer, Youtube, etc.)")
        )

    test= models.BooleanField(
        blank=True,
        default=False,
        help_text=_('boolean to avoid celery when testing')
        )  

    class Meta:
        ordering = ['-date_modified']
        verbose_name = _('item')

    def __str__(self):
        if self.title:
            return '_'.join([str(self.title), str(self.uuid)[:4]])
        else:
            return str(self.uuid)

    def results(self):
        return [result for result in self.results.all()]

    def lock_setter(self, lock):
        self.lock = lock
        self.save()

    def get_source_from_id(self, download=True):
        # check if item has not already an audio source url or file,
        # has an external id to retrieve audio source,
        # and a has provider that gives free access to audio sources.

        source = ''
        if not (self.source_url or self.source_file) and \
                self.external_id and \
                self.provider and self.provider.source_access:
            try:
                source = self.provider.get_source_from_id(
                        self.external_id, download
                        )
            except timeside.core.exceptions.ProviderError as e:
                app_logger.warning(e)
                self.external_uri = ''
                self.external_id = ''
        return source

    def get_source_from_uri(self, download=True):
        # check if item has not already an audio source url or file,
        # has an external uri to retrieve audio source,
        # and a has provider that gives free access to audio sources.
        # TODO: merge this with get_source_from_id

        source = ''
        if not (self.source_url or self.source_file) and \
                self.external_uri and \
                self.provider and \
                self.provider.source_access:
            try:
                source = self.provider.get_source_from_url(
                        self.external_uri, download
                        )
            except timeside.core.exceptions.ProviderError as e:
                app_logger.warning(e)
                self.external_uri = ''
                self.external_id = ''
        return source

    def get_external_id(self):
        """
        """

        external_id = ''
        if not (self.source_url or self.external_id) and self.external_uri:
            try:
                external_id = self.provider.get_id_from_url(
                    self.external_uri
                    )
            except timeside.core.exceptions.ProviderError as e:
                app_logger.warning(e)
                self.external_uri = ''
                self.external_id = ''
        return external_id

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

        result_path = os.path.join(RESULTS_ROOT, str(self.uuid))
        if not os.path.exists(result_path):
            os.makedirs(result_path)
        return result_path

    def get_audio_duration(self, force=False):
        """
        Return item audio duration
        """

        audio_duration = None
        if (
            (force or not self.audio_duration)
            and self.source_file
           ):
            decoder = timeside.core.get_processor(DEFAULT_DECODER)(
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
            decoder = timeside.core.get_processor(DEFAULT_DECODER)(
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
        preset, c = Preset.objects.get_or_create(processor=processor)
        experience = preset.get_single_experience()
        task, c = Task.objects.get_or_create(item=self, experience=experience)
        if not c:
            task.run()

    def run(self, experience, task=None, item=None):
        result_path = self.get_results_path()
        # get audio source
        uri = self.get_uri()

        if not uri:
            raise ValueError('Item does not have any source URI, nothing can be run.')

        # decode audio source
        # TODO: use get_processor

        if task and experience and item:

            task_uuid = str(task.uuid)
            experience_uuid = str(experience.uuid)
            item_uuid = str(item.uuid)

            def progress_callback(completion):
                r.publish(
                    'timeside-experience-progress',

                    'cgerard' +
                    ":" + task_uuid +
                    ":" + experience_uuid +
                    ":" + item_uuid +
                    ":" + str(completion)
                )
        else:
            progress_callback = None 

        if DEFAULT_DECODER == 'aubio_decoder':
            decoder = timeside.plugins.decoder.aubio.AubioDecoder(
                uri=uri,
                sha1=self.sha1,
                progress_callback=progress_callback
                )
        else:
            decoder = timeside.plugins.decoder.file.FileDecoder(
                uri=uri,
                sha1=self.sha1,
                progress_callback=progress_callback
                )

        presets = {}
        pipe = decoder
        parent_analyzers = []

        # search for parent analyzer presets
        # not to add as duplicates in the pipe
        for preset in experience.presets.all():
            proc = preset.processor.get_processor()
            if proc.type in ['analyzer', 'grapher']:
                proc = proc(**json.loads(preset.parameters))
                if 'analyzer' in proc.parents:
                    parent_analyzers.append(proc.parents['analyzer'])

        for preset in experience.presets.all():
            # get core audio metaProcessor
            # corresponding to preset.processor.pid
            proc = preset.processor.get_processor()
            if proc.type == 'encoder':
                result, c = Result.objects.get_or_create(preset=preset,
                                                         item=self)
                media_file = '.'.join([str(result.uuid),
                                       proc.file_extension()])
                result.file = os.path.join(result_path, media_file).replace(
                    settings.MEDIA_ROOT, ''
                    )
                result.save()
                # instantiate a core processor of an encoder
                proc = proc(result.file.path, overwrite=True,
                            streaming=False)
                worker_logger.info(f'Run {str(proc)} on {str(self)}')
            elif proc.type in ['analyzer', 'grapher']:
                # instantiate a core processor of an analyzer or a grapher
                proc = proc(**json.loads(preset.parameters))
                worker_logger.info(
                    f'Run {proc} on {self} with {preset.parameters}'
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
                item=self
                )

            if not hasattr(proc, 'external'):
                hdf5_file = str(result.uuid) + '.hdf5'
                result.hdf5 = os.path.join(
                    result_path,
                    hdf5_file
                    ).replace(settings.MEDIA_ROOT, '')
                proc.results.to_hdf5(result.hdf5.path)
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
                                                         item=self)
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
                result = Result.objects.get(preset=preset, item=self)
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

    def save(self, **kwargs):
        if not self.title:
            self.title = str(self.uuid)
        super(Item, self).save(**kwargs)


def item_post_save(sender, **kwargs):
    """ """
    from timeside.server.tasks import item_post_save_async
    instance = kwargs['instance']
    item_post_save_async.delay(uuid=instance.uuid)

post_save.connect(item_post_save, sender=Item)


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


@python_2_unicode_compatible
class Processor(UUID):

    pid = models.CharField(_('pid'), max_length=128)
    version = models.CharField(_('version'), max_length=64, blank=True)
    name = models.CharField(_('name'), max_length=256, blank=True)

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
        return self.get_processor().get_parameters_schema()

    def get_parameters_default(self):
        return self.get_processor().get_parameters_default()


@python_2_unicode_compatible
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
    parameters = models.TextField(_('Parameters'), blank=True, default='{}')
    # parameters = models.TextField(
    # _('Parameters'), blank=False, default='{}', null=False
    # )
    # TODO : turn this filed into a JSON Field
    # see : http://stackoverflow.com/questions/22600056/django-south-changing-field-type-in-data-migration   # noqa

    class Meta:
        verbose_name = _('Preset')
        verbose_name_plural = _('Presets')
        ordering = ['processor__pid',]

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
        ordering = ['-date_added']

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


@python_2_unicode_compatible
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
        help_text=_(cleandoc(f"""
            Task's status:\n
            failed: {_FAILED}\n
            draft: {_DRAFT}\n
            pending: {_PENDING}\n
            running: {_RUNNING}\n
            done: {_DONE}
            """))
        )

    test = models.BooleanField(
        blank=True,
        default=False,
        help_text=_('boolean to avoid celery when testing')
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
        else:
            return '_'.join(
                [str(self.selection), str(self.experience), str(self.uuid)[:4]]
                )

    def status_setter(self, status):
        self.status = status
        self.save()

    def is_done(self):
        return (self.status == _DONE)

    def run(self, wait=False, streaming=False):
        self.status_setter(_RUNNING)

        from timeside.server.tasks import task_run
        if not self.test:
            task_run.delay(task_id=str(self.uuid))
        else:
            task_run(task_id=str(self.uuid),test=True)

        if wait:
            status = Task.objects.get(uuid=str(self.uuid)).status
            while (status != _DONE):
                time.sleep(0.5)
                worker_logger.info('WAITING')
                status = Task.objects.get(uuid=str(self.uuid)).status


def task_run(sender, **kwargs):
    task = kwargs['instance']
    if task.status == _PENDING:
        task.run()

post_save.connect(task_run, sender=Task)



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
    test= models.BooleanField(
        blank=True,
        default=False,
        help_text=_('boolean to avoid celery when testing')
        )  

    parameters_schema = jsonfield.JSONField(default=DEFAULT_SCHEMA())

    class Meta:
        verbose_name = _('Analysis')
        verbose_name_plural = _('Analyses')
        ordering = ['title']


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
        blank=False,
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
        return self.analysis.title + ' - ' + self.item.title


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
