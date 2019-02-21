from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.exceptions import MultipleObjectsReturned

import os
import timeside.core
from timeside.server.models import Selection, Item, Processor, Preset, Experience, Task, Analysis, SubProcessor
from timeside.server.models import _PENDING, _DONE
from timeside.core.tools.test_samples import generateSamples
import simplejson as json


class Command(BaseCommand):
    help = "Create and run the WASABI experience on a given directory or a selection"
    
    media_root = os.path.normpath(settings.MEDIA_ROOT)
    experience_processors = ['aubio_temporal', 'aubio_pitch', 'essentia_dissonance', ]
    #experience_processors = ['ircam_music_descriptor', ]
    processor_blacklist = ['decoder', 'live', 'gain', 'vamp']

    def add_arguments(self, parser):
        parser.add_argument('-s', '--selection_title',
            dest='selection_title',
            help='define the title of the selection')

        parser.add_argument('-e', '--experience_title',
            dest='experience_title',
            help='define the title of the experience')

        parser.add_argument('-m', '--media_directory',
            dest='media_directory',
            help='define the media directory')

        parser.add_argument('-l', '--log',
            dest='log',
            help='define log file')

        parser.add_argument('-f', '--force',
            action='store_true',
            dest='force',
            help='Force overwrite data')

        parser.add_argument('-c', '--cleanup',
            action='store_true',
            dest='cleanup',
            help='Cleanup result data')

    def write_file(self, item, media):
        filename = media.split(os.sep)[-1]
        if os.path.exists(media):
            if not item.file or self.force:
                if not self.media_root in self.source_dir:
                    print("file not in MEDIA_ROOT, copying...")
                    f = open(media, 'r')
                    if not self.dry_run:
                        file_content = ContentFile(f.read())
                        item.source_file.save(filename, file_content)
                        item.save()
                    f.close()
                else:
                    print("file in MEDIA_ROOT, linking...")
                    path = media[len(self.media_root)+1:]
                    if not self.dry_run:
                        item.source_file = path
                        item.save()

    def create_selection(self):
        self.selection, c = Selection.objects.get_or_create(title=self.selection_title)
        items = self.selection.items.all()

        for root, dirs, files in os.walk(self.media_directory):
            for filename in files:
                path = root + os.sep + filename
                filename_pre, ext = os.path.splitext(filename)
                item_title = filename_pre
                item, c = Item.objects.get_or_create(title=item_title, source_file=path)
                    
                if not item in items:
                    self.selection.items.add(item)
                
                if self.cleanup:
                    for result in item.results.all():
                        result.delete()

    def create_experience(self):
        presets = []
        processors = timeside.core.processor.processors(timeside.core.api.IProcessor)
        for proc in processors:
            trig = True
            # print(proc.id())
            if proc.id() in self.experience_processors:
                for processor in self.processor_blacklist:
                    if processor in proc.id():
                        trig = False
                if trig:
                    processor, c = Processor.objects.get_or_create(pid=proc.id())
                    try:
                        preset, c = Preset.objects.get_or_create(processor=processor, parameters='{}')
                        presets.append(preset)
                    except Preset.MultipleObjectsReturned:
                        print(Preset.objects.filter(processor=processor, parameters='{}'))

        self.experience, c = Experience.objects.get_or_create(title=self.experience_title)
        for preset in presets:
            if not preset in self.experience.presets.all():
                self.experience.presets.add(preset)
        
    def handle(self, *args, **options):
        self.selection_title = options.get('selection_title')
        self.experience_title = options.get('experience_title')
        self.media_directory =  options.get('media_directory')
        self.force = options.get('force')
        self.cleanup = options.get('cleanup')

        self.create_selection()
        self.create_experience()

        task, c = Task.objects.get_or_create(experience=self.experience, selection=self.selection)
        if c or task.status != _DONE or self.force:
            task.status = _PENDING
            task.save()

        