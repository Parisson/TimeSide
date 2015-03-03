from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from timeside.server.models import Task


class Command(BaseCommand):
    help = "Re-run all tasks"

    def handle(self, *args, **options):
        for task in Task.objects.all():
            task.status_setter(2)
