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
from timeside.core.tools.test_samples import generateSamples
import simplejson as json


class Command(BaseCommand):

    def handle(self, *args, **options):
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
            except:
                pass
