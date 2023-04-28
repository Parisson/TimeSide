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
    help = "Setup all processors and presets from timeside.core"
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

    def analysis_cleanup(self):
        for analysis in Analysis.objects.all():
            analysis.delete()

    def handle(self, *args, **options):
        verbosity = options.get('verbosity')
        if verbosity:
            print("---------------------------")
            print("--  CREATE PRESETS       --")
            print("---------------------------")

        # ---------- Test Selection ----------


        presets = []
        blacklist = ['decoder', 'live', 'gain', 'vamp', 'yaafe']
        processors = timeside.core.processor.processors(
            timeside.core.api.IProcessor
            )
        graphers = timeside.core.processor.processors(
            timeside.core.api.IGrapher
            )


        if verbosity:
            print(" - created presets:")

        for proc in processors:
            trig = True
            for black in blacklist:
                if black in proc.id():
                    trig = False
            if trig:
                processor, c = Processor.objects.get_or_create(
                    pid=proc.id(),
                    version=proc.version()
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
                                                                                processor=processor
                                                                                )

                            analysis, c = Analysis.objects.get_or_create(
                                                                        sub_processor=sub_processor,
                                                                        preset=preset,
                                                                        title=proc._grapher_name+' grapher',
                                                                        render_type=1
                                                                        )

                    else:
                        print(processor)
                        preset, created = Preset.objects.get_or_create(processor=processor,
                                                                    parameters=json.dumps(processor.get_parameters_default()))
                        if created and verbosity:
                                            print("    " + str(preset))
                    presets.append(preset)
                except Preset.MultipleObjectsReturned:
                    print(Preset.objects.filter(processor=processor, parameters='{}'))

        # ------------ Analyzers -------------
        analyzers = timeside.core.processor.processors(
            timeside.core.api.IAnalyzer
            )
        nb=0
        for a in analyzers :

            try :
                processor,c= Processor.objects.get_or_create(
                            pid=a.id(),
                            version=a.version()
                            )

                preset,c= Preset.objects.get_or_create(
                            processor=processor,
                            parameters=json.dumps(a.get_parameters_default())
                            )

                sub_processor,c= SubProcessor.objects.get_or_create(
                            sub_processor_id=a.id(),
                            processor=processor
                            )

                analysis,c = Analysis.objects.get_or_create(
                            sub_processor=sub_processor,
                            preset=preset,
                            title=a.name(),
                            )
            except : pass

        # ------------ Providers -------------
        providers = timeside.core.provider.providers(timeside.core.api.IProvider)

        for prov in providers:
            provider, c = Provider.objects.get_or_create(
                pid=prov.id(),
                source_access=prov.access(),
                description=prov.description(),
                name=prov.name()
                )

        # ---------- Experience All ----------
        experience, c = Experience.objects.get_or_create(title='All')
        for preset in presets:
            if not preset in experience.presets.all():
                experience.presets.add(preset)

        # ------------- Analysis -------------
        for analysis in Analysis.objects.all():
            analysis.parameters_schema = analysis.preset.processor.get_parameters_schema()
            analysis.save()
