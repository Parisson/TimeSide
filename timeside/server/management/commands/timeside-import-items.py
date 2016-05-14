from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from timeside.server.models import *
import os, sys

try:
    from django.utils.text import slugify
except ImportError:
    def slugify(string):
        killed_chars = re.sub('[\(\),]', '', string)
        return re.sub(' ', '_', killed_chars)

def beautify(string):
    return os.path.splitext(string)[0].replace('_',' ')


class Command(BaseCommand):
    help = """import media files from the media directory into some items
            and create a selection (no file copy)"""
    args = "selection_title media_dir"

    def handle(self, *args, **options):
        selection_title = args[-2]
        import_dir = os.path.abspath(args[-1])
        media_dir = os.path.normpath(settings.MEDIA_ROOT)

        if not media_dir in import_dir:
            sys.exit('This directory is not in the MEDIA_ROOT directory')

        selection, c = Selection.objects.get_or_create(title=selection_title)
        if c:
            print 'Selection "' + selection_title + '" created'

        for root, dirs, files in os.walk(import_dir):
            for filename in files:
                path = os.path.join(root, filename)
                os.path.relpath(path, media_dir)
                relpath = path[len(media_dir)+1:]
                name, ext = os.path.splitext(filename)
                title = unicode(selection_title + '_' + filename)
                item, c = Item.objects.get_or_create(title=title, source_file=relpath)
                if c:
                    print 'Item "' + title + '" created'
                if not item in selection.items.all():
                    selection.items.add(item)
                    print 'Item "' + title + '" added to selection "' + selection_title +'"'
