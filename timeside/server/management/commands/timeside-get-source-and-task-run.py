from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from timeside.server.models import Task, Item
import datetime


class Command(BaseCommand):
    help = "Re-save empty source_file items added from yesterday to now"

    def handle(self, *args, **options):
        yesterday = datetime.datetime.now - datetime.timedelta(days=1)
        items = Item.objects.filter(source_file__isnull=True, \
                                date_added__gte=yesterday)
        for item in items:
            item.save()

