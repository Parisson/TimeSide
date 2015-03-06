from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

import os
import timeside.core
from timeside.server.models import *
from timeside.core.tools.test_samples import generateSamples


class Command(BaseCommand):
    help = "Setup and run a boilerplate for testing"

    def cleanup(self):
        for processor in Processor.objects.all():
            processor.delete()
        for result in Result.objects.all():
            result.delete()

    def handle(self, *args, **options):
        # NOT for production
        self.cleanup()

        presets = []
        blacklist =['decoder', 'live', 'gain', 'yaafe']
        processors = timeside.core.processor.processors(timeside.core.api.IProcessor)
        for proc in processors:
            trig = True
            for black in blacklist:
                if black in proc.id():
                    trig = False
            if trig:
                processor, c = Processor.objects.get_or_create(pid=proc.id())
                preset, c = Preset.objects.get_or_create(processor=processor, parameters='{}')
                presets.append(preset)

        media_dir = 'items' + os.sep + 'tests'
        samples_dir = settings.MEDIA_ROOT + media_dir
        samples = generateSamples(samples_dir=samples_dir)
        selection, c = Selection.objects.get_or_create(title='Tests')

        for sample in samples.iteritems():
            filename, path = sample
            title = os.path.splitext(filename)[0]
            path = media_dir + os.sep + filename
            item, c = Item.objects.get_or_create(title=title, file=path)
            if not item in selection.items.all():
                selection.items.add(item)

        experience, c = Experience.objects.get_or_create(title='All')
        for preset in presets:
            if not preset in experience.presets.all():
                experience.presets.add(preset)

        task, c = Task.objects.get_or_create(experience=experience, selection=selection)
        task.status_setter(2)
