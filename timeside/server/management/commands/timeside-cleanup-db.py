from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.exceptions import MultipleObjectsReturned

import os
import timeside.core
from timeside.server.models import Selection, Item
from timeside.server.models import Processor, Preset, Result, Experience, Task, Analysis, SubProcessor
from timeside.server.models import _PENDING, _DONE
from timeside.core.tools.test_samples import generateSamples


class Command(BaseCommand):
    help = "Clean-up Timeside database by deleting all objects"

    def handle(self, *args, **options):
        for processor in Processor.objects.all():
            processor.delete()
        for result in Result.objects.all():
            result.delete()
        for preset in Preset.objects.all():
            preset.delete()
        for exp in Experience.objects.all():
            exp.delete()
        # for task in Task.objects.all():
        #    task.delete()
        for analysis in Analysis.objects.all():
            analysis.delete()
        for subproc in SubProcessor.objects.all():
            subproc.delete()
