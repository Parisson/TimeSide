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

def get_or_run_proc_result(pid, item, parameters='{}'):

    # Get or Create Processor
    processor, c = Processor.objects.get_or_create(pid=pid)

    # Get or Create Preset with processor
    preset, c = Preset.get_first_or_create(processor=processor,
                                    parameters=parameters)

    # Get or create Result with preset and item
    result, created = Result.get_first_or_create(preset=preset, 
                                   item=item)

    while not created and (not result.hdf5 or not os.path.exists(result.hdf5.path)):
        # Result exists but does not content any file or the path points a deleted File
        result.delete()
        result, created = Result.get_first_or_create(preset=preset, 
                                   item=item)
    
    if created: 
        task, c = Task.get_first_or_create(experience=preset.get_single_experience(),
                                                        selection=item.get_single_selection())
        task.run(wait=True)

    return result
    
# TODO def get_or_run_proc_item(pid, version, item, prarameters={}):
# don't run the task if results exist for a proc with its version