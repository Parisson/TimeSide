# -*- coding: utf-8 -*-
import os

import timeside.core
import json
from timeside.core.api import IEncoder
from timeside.server.models import Processor, Preset, Result, Task

TS_ENCODERS = timeside.core.processor.processors(IEncoder)
TS_ENCODERS_EXT = {encoder.file_extension(): encoder.id()
                   for encoder in TS_ENCODERS
                   if encoder.file_extension()}

def get_or_run_proc_result(pid, item, parameters={}):

    # Get or Create Processor
    processor, created = Processor.objects.get_or_create(pid=pid)
    # Get or Create Preset with processor
    presets = Preset.objects.filter(processor=processor,
                                    parameters=json.dumps(parameters))
    if presets:
        preset = presets[0]
    else:
        preset = Preset(processor=processor,
                        parameters=json.dumps(parameters))
        preset.save()
                
    # preset, created = Preset.objects.get_or_create(processor=processor, parameters=parameters)
    # Get Result with preset and item
    try:
        result = Result.objects.get(item=item, preset=preset)
        if not os.path.exists(result.hdf5.path):
            # Result exists but not file (may have been deleted)
            result.delete()
            return get_or_run_proc_result(pid, item, parameters)
        # Result and file exist --> OK
        return result
    except Result.DoesNotExist:
        # Result does not exist
        # the corresponding task has to be created and run
        task, created = Task.objects.get_or_create(experience=preset.get_single_experience(),
                                                   selection=item.get_single_selection())
        task.run(wait=True)
    return  get_or_run_proc_result(pid, item, parameters)
            #response = StreamingHttpResponse(streaming_content=stream_from_task(task),
            #                                 content_type=mime_type)
            #return response
