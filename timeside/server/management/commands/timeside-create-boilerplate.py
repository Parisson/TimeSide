from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.exceptions import MultipleObjectsReturned

import os
import timeside.core
from timeside.server.models import Selection, Item
from timeside.server.models import Processor, Provider, Preset, Experience, Task, Analysis, SubProcessor
from timeside.server.models import _PENDING, _DONE
from timeside.core.tools.test_samples import generateSamples
import simplejson as json


class Command(BaseCommand):
    help = "Setup and run a boilerplate for testing"
    cleanup = True

    def processor_cleanup(self):
        for processor in Processor.objects.all():
            processor.delete()

    def result_cleanup(self):
        for result in Result.objects.all():
            result.delete()

    def handle(self, *args, **options):
        media_dir = os.path.join('items', 'tests')
        samples_dir = os.path.join(settings.MEDIA_ROOT, media_dir)

        Selection.objects.get_or_create(title='WASABI')
        selection, c = Selection.objects.get_or_create(title='Tests')
        if c | (selection.items.count() == 0):
            print "---------------------------"
            print "-- CREATE BOILERPLATE    --"
            print "---------------------------"
            print " -  generate samples"

            samples = generateSamples(samples_dir=samples_dir)

            for sample in samples.iteritems():
                filename, path = sample
                title = os.path.splitext(filename)[0]
                path = os.path.join(media_dir, filename)
                item, c = Item.objects.get_or_create(title=title, source_file=path)
                if not item in selection.items.all():
                    selection.items.add(item)
                if self.cleanup:
                    for result in item.results.all():
                        result.delete()

        presets = []
        blacklist = ['decoder', 'live', 'gain', 'vamp']
        processors = timeside.core.processor.processors(timeside.core.api.IProcessor)

        for proc in processors:
            trig = True
            for black in blacklist:
                if black in proc.id():
                    trig = False
            if trig:
                processor, c = Processor.objects.get_or_create(pid=proc.id())
                try:
                    preset, c = Preset.objects.get_or_create(processor=processor, parameters='{}')
                    presets.append(preset)
                except Preset.MultipleObjectsReturned:
                    print Preset.objects.filter(processor=processor, parameters='{}')

        providers = timeside.core.provider.providers(timeside.core.api.IProvider)

        for prov in providers:
            provider, c = Provider.objects.get_or_create(pid=prov.id())

        experience, c = Experience.objects.get_or_create(title='All')
        for preset in presets:
            if not preset in experience.presets.all():
                experience.presets.add(preset)

        task, c = Task.objects.get_or_create(experience=experience, selection=selection)
        if c | task.status != _DONE:
            task.status = _PENDING
            task.save()

        # ---- Graphers -----
        for grapher in timeside.core.processor.processors(timeside.core.api.IGrapher):
            if hasattr(grapher, '_from_analyzer') and grapher._from_analyzer and not(grapher._staging):

                processor, c = Processor.objects.get_or_create(pid=grapher._analyzer.id())
                try:
                    preset, c = Preset.objects.get_or_create(processor=processor,
                                                             parameters=json.dumps(grapher._analyzer_parameters))
                except MultipleObjectsReturned:
                    print Preset.objects.get(processor=processor,
                                             parameters=grapher._analyzer_parameters)

                sub_processor, c = SubProcessor.objects.get_or_create(sub_processor_id=grapher._result_id,
                                                                      processor=processor)

                analysis, c = Analysis.objects.get_or_create(sub_processor=sub_processor,
                                                             preset=preset,
                                                             title=grapher._grapher_name)

        for analysis in Analysis.objects.all():
            analysis.parameters_schema = analysis.preset.processor.get_parameters_schema()
            analysis.save()
