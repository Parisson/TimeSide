from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from timeside.server.models import *
import os, sys, csv

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

    def add_arguments(self, parser):
        parser.add_argument(
            '-s',
            '--selection_title',
            dest='selection_title',
            )

        parser.add_argument(
            '-d',
            '--import_dir',
            dest='import_dir',
            )

        parser.add_argument(
            '-c',
            '--csv_file',
            dest='csv_file',
            )

        parser.add_argument(
            '-p',
            '--provider_name',
            dest='provider_domain',
            )

    def handle(self, *args, **kwargs):
        csv_file = kwargs.get('csv_file')
        selection_title = kwargs.get('selection_title')
        import_dir = os.path.abspath(kwargs.get('import_dir'))
        provider_domain = kwargs.get('provider_domain')
        media_dir = os.path.normpath(settings.MEDIA_ROOT)

        print(csv_file)

        if not media_dir in import_dir:
            sys.exit('This directory is not in the MEDIA_ROOT directory')

        metadata_d = {}
        csv_file_it = open(csv_file)
        metadata = csv.DictReader(csv_file_it)

        for track in metadata:
            # id,artist,album,title,url,picture,summary
            metadata_d[track['id']] = {
                "artist": track['artist'],
                "album": track['album'],
                "title": track["title"],
                "url": track["url"],
                "picture": track["picture"],
                "summary": track["summary"]
            }

        selection, c = Selection.objects.get_or_create(title=selection_title)
        if c:
            print('Selection "' + selection_title + '" created')

        provider, c = Provider.objects.get_or_create(
            name=provider_domain,
            domain=provider_domain,
            pid=provider_domain
            )

        existing_items_ids = [item.external_id for item in Item.objects.all()]
        items_in_selection = selection.items.all()

        for root, dirs, files in os.walk(import_dir):
            for filename in files:
                path = os.path.join(root, filename)
                os.path.relpath(path, media_dir)
                relpath = path[len(media_dir)+1:]
                name, ext = os.path.splitext(filename)
                external_id = name
                meta_track = metadata_d[external_id]
                if not external_id in existing_items_ids:
                    item = Item(external_id=external_id)
                    text = "created"
                else:
                    item = Item.objects.get(external_id=external_id)
                    text = "updated"
                    print('Item "' + id + '" updated')

                item.title = meta_track['title']
                item.artist = meta_track['artist']
                item.album = meta_track['album']
                item.external_uri = meta_track['url']
                item.picture_url = meta_track['picture']
                item.source_file = relpath
                item.save()

                print('Item ' + id + ' ' + text)

                if not item in items_in_selection:
                    selection.items.add(item)
                    print('Item ' + item.external_id + ' added to selection')

                else:
                    print('Item ' + item.external_id + ' already in selection')


