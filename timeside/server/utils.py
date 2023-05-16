# -*- coding: utf-8 -*-
import os

import timeside.core
import json

from django.conf import settings

from timeside.core.api import IEncoder
from timeside.server.models import Processor, Preset, Result, Task

from rest_framework.views import exception_handler
from rest_framework.renderers import BaseRenderer, JSONRenderer

TS_ENCODERS = timeside.core.processor.processors(IEncoder)
TS_ENCODERS_EXT = {encoder.file_extension(): encoder.id()
                   for encoder in TS_ENCODERS
                   if encoder.file_extension()}


def get_or_run_proc_result(pid, item, parameters='{}', user=None):
    # Get or Create Processor
    processor = Processor.get_first(pid=pid)

    if not parameters:
        parameters = processor.get_parameters_default()

    # Get or Create Preset with Processor
    preset, c = Preset.get_first_or_create(
        processor=processor,
        parameters=parameters
        )

    return get_result(item, preset, user=user, wait=True)

# TODO def get_or_run_proc_item(pid, version, item, prarameters={}):
# don't run the task if results exist for a proc with its version


def get_result(item, preset, user=None, wait=True):
    # Get or create Result with preset and item
    result, created = Result.get_first_or_create(
        preset=preset,
        item=item
        )

    if user.is_authenticated:
        u = user
    else:
        u = None

    if created or \
            not settings.CACHE_RESULT or \
            (
                not result.has_file() and
                not result.has_hdf5()
            ):


        task, c = Task.get_first_or_create(
            experience=preset.get_single_experience(),
            item=item,
            author=u
            )

        task.save()
        task.run()

        # SMELLS: might not get the last good result
        # TODO: manage Task running return for Analysis through API
        result, created = Result.get_first_or_create(
            preset=preset,
            item=item
            )
        
        return result

    else:
        return result


def custom_exception_handler(exc, context):
    """ Switch from PNGRenderer to JSONRenderer for exceptions """
    if context['request'].accepted_renderer.format == 'png':
        context['request'].accepted_renderer = JSONRenderer()

    return exception_handler(exc, context)


class PNGRenderer(BaseRenderer):
    """ Custom renderer for hdf5 results bitmap serialization """
    media_type = 'image/png'
    format = 'png'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data


class AudioRenderer(BaseRenderer):
    """ Custom renderer for item's audio source transcode view """
    media_type = 'audio/*'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data
