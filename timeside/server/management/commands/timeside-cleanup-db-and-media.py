from django.core.management.base import BaseCommand
from django.conf import settings

import os

from .remove_empty_folders import removeEmptyFolders

from timeside.server.models import (
    Result,
    _DONE,
    _DRAFT,
    _FAILED,
    Selection,
    Item,
)


class Command(BaseCommand):
    help = """Clean-up inconsistent data into Timeside's db.
            Remove any file in MEDIA_ROOT
            that have no Objects referring to it."""

    def handle(self, *args, **options):
        media_paths = set()
        # delete former singleton Selection
        for selection in Selection.objects.all():
            if 'Singleton selection for item' in selection.title:
                selection.delete()
        # delete results that are not pointing to a real file or hdf5
        # add file or hdf5 to media_paths otherwise
        for result in Result.objects.all():
            if result.status == _DONE:
                if result.has_file():
                    media_paths.add(result.file.path)
                elif result.has_hdf5():
                    media_paths.add(result.hdf5.path)
                else:
                    result.delete()
            elif result.status in [_DRAFT, _FAILED]:
                result.delete()
            else:
                continue
        # delete items that are pointing to a non existing audio file
        # add file to media_paths otherwise
        for item in Item.objects.all():
            if item.source_file:
                if os.path.exists(item.source_file.path):
                    media_paths.add(item.source_file.path)
                else:
                    item.delete()
            else:
                continue
        # remove any result hdf5, xml, json or png file and any audio file
        # that are not referred by any Result or Item object
        for root, dirs, files in os.walk(settings.MEDIA_ROOT):
            for f in files:
                path = os.path.join(root, f)
                if path not in media_paths:
                    os.remove(path)
        # TODO remove empty folders

