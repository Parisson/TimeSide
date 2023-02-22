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
    help = "Run a timeside task"

    def add_arguments(self, parser):
        parser.add_argument('-u', '--uuid',
            dest='uuid',
            help='define the uuid of the task')

    def handle(self, *args, **options):
        self.uuid = options.get('uuid')
        task = Task.objects.get(uuid=self.uuid)
        task.status = _PENDING
        task.save()

