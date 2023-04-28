from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.exceptions import MultipleObjectsReturned

import os
import timeside.core
from timeside.server.models import RENDER_TYPES, Selection, Item
from timeside.server.models import Processor, Provider, Preset, Experience, Task, Analysis, SubProcessor, Result
from timeside.server.models import _PENDING, _DONE
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

    def experience_cleanup(self):
        for experience in Experience.objects.all():
            experience.delete()

    def preset_cleanup(self):
        for preset in Preset.objects.all():
            preset.delete()

    def task_cleanup(self):
        for task in Task.objects.all():
            task.delete()

    def analysis_cleanup(self):
        for analysis in Analysis.objects.all():
            analysis.delete()

    def generate_test_samples(self):
        from timeside.core.tools.test_samples import generateSamples
        media_dir = os.path.join('items', 'tests')
        samples_dir = os.path.join(settings.MEDIA_ROOT, media_dir)
        selection, c = Selection.objects.get_or_create(title='Tests')
        if c | (selection.items.count() == 0):
            if verbosity:
                print("generate samples")
            samples = generateSamples(samples_dir=samples_dir)
            for sample in samples.items():
                filename, path = sample
                title = os.path.splitext(filename)[0]
                path = os.path.join(media_dir, filename)
                item, c = Item.objects.get_or_create(
                    title=title, source_file=path
                    )
                if not item not in selection.items.all():
                    selection.items.add(item)
                if self.cleanup:
                    for result in item.results.all():
                        result.delete()

    def analyze_test_samples(self):
        task, c = Task.objects.get_or_create(
            experience=experience,
            selection=selection
            )
        if verbosity and c:
            print(' - created task:')
            print(task)
        if c | task.status != _DONE:
            task.status = _PENDING
            task.save()

    def handle(self, *args, **options):
        verbosity = options.get('verbosity')
        if verbosity:
            print("---------------------------")
            print("--  CREATE BOILERPLATE   --")
            print("---------------------------")

            presets = []
            blacklist = ['decoder', 'live', 'gain', 'vamp', 'yaafe']
            processors = timeside.core.processor.processors(
                timeside.core.api.IProcessor
                )
            graphers = timeside.core.processor.processors(
                timeside.core.api.IGrapher
                )

            if verbosity:
                print("create presets:")
                
            for proc in processors:
                trig = True
                for black in blacklist:
                    if black in proc.id():
                        trig = False
                if trig:
                    print(proc.id())
                    processor, c = Processor.objects.get_or_create(
                        pid=proc.id(),
                        version=proc.version(),
                        description=proc.description(),
                        )
                    
                    try:
                    
                           
                        if proc in graphers:
                            
                            # TODO: resolve missing Graphers !!! maybe if hasattrb ... else : get_or_greate()
                            # ---- Graphers -----
                            if hasattr(proc, '_from_analyzer') and proc._from_analyzer and not(proc._staging):
                                try:
                                    parameters = json.dumps(
                                        proc._analyzer_parameters
                                        )
                                    preset, created = Preset.objects.get_or_create(
                                                                            processor=processor,
                                                                            parameters=parameters
                                                                            )
                                    if created and verbosity:
                                        print("    " + str(preset))

                                except MultipleObjectsReturned:
                                    print(Preset.objects.get(
                                                            processor=processor,
                                                            parameters=json.dumps(
                                                                proc._analyzer_parameters
                                                                )
                                                            )
                                                        )

                                sub_processor, c = SubProcessor.objects.get_or_create(
                                                                                    sub_processor_id=proc._result_id,
                                                                                    processor=processor,
                                                                                    )

                                analysis, c = Analysis.objects.get_or_create(
                                                                            sub_processor=sub_processor,
                                                                            preset=preset,
                                                                            title=proc._grapher_name+' grapher',
                                                                            render_type=1
                                                                            )
                           
                        else:
                            preset, created = Preset.objects.get_or_create(processor=processor,
                                                                        parameters=processor.get_parameters_default())
                            if created and verbosity:
                                                print("    " + str(preset))
                        presets.append(preset)
                    except Preset.MultipleObjectsReturned:
                        print(Preset.objects.filter(processor=processor, parameters='{}'))
                    
            # ------------ Analyzers -------------
            analyzers = timeside.core.processor.processors(
                timeside.core.api.IAnalyzer
                )
            for a in analyzers :
                print(a)
                try :
                    processor,c= Processor.objects.get_or_create(
                                pid=a.id(),
                                version=a.version(),
                                description=a.description(),
                                )
            
                    preset,c= Preset.objects.get_or_create(
                                processor=processor,
                                parameters=a.get_parameters_default()
                                )

                    sub_processor,c= SubProcessor.objects.get_or_create(
                                sub_processor_id=a.id(),
                                processor=processor,
                                description=a.description(),
                                )
                                
                    analysis,c = Analysis.objects.get_or_create(
                                sub_processor=sub_processor,
                                preset=preset,
                                title=a.name(),
                                description=a.description(),
                                )
                except:
                    continue
                
            # ------------ Providers -------------
            providers = timeside.core.provider.providers(timeside.core.api.IProvider)

            for prov in providers:
                provider, c = Provider.objects.get_or_create(
                    pid=prov.id(),
                    source_access=prov.access(),
                    description=prov.description(),
                    name=prov.name(),
                    domain=prov.domain(),
                    )

            # ------------- Analysis -------------
            for analysis in Analysis.objects.all():
                print(analysis)
                analysis.parameters_schema = analysis.preset.processor.get_parameters_schema()
                analysis.save()


            # ---------- Experience All ----------
            experience, c = Experience.objects.get_or_create(title='All')
            for preset in presets:
                if not preset in experience.presets.all():
                    experience.presets.add(preset)


