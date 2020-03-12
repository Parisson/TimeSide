from django.core.management.base import BaseCommand

from timeside.server.models import (
    Item,
    Provider,
    Selection,
    Experience,
)

from os.path import (
    join,
    dirname,
    realpath
)
import random
import timeside.core
import json
import sys

# DALI columns descriptions
DALI_ID, WASABI_ID, NAME, DEEZER_ID, YOUTUBE_ID, WORKING = 0, 1, 2, 3, 4, 5

# List of available providers' pid
providers = tuple(prov.pid for prov in Provider.objects.all())


class Command(BaseCommand):
    help = """
    Create a selection of n items from random DALI's IDs
    """

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument(
            'pid',
            type=str,
            choices=providers,
            help='provider id'
            )

        # Named (optional) arguments
        parser.add_argument(
            '-s',
            '--selection_title',
            dest='selection_title',
            help='define the title of the selection',
            default='tracks from DALI'
            )

        parser.add_argument(
            '-nb',
            '--item_number',
            dest='item_number',
            type=int,
            help='define the number of item to include in the selection',
            default=10
            )

        parser.add_argument(
            '-a',
            '--all',
            dest='all',
            type=bool,
            help="determine if all DALI corpus is included",
            default=False
            )

    def handle(self, *args, **options):
        self.pid = options.get('pid')
        self.selection_title = options.get('selection_title')
        self.item_number = options.get('item_number')
        self.all = options.get('all')

        if 'deezer' in self.pid:
            id_ind, desc_name, desc_ind = DEEZER_ID, 'YOUTUBE_ID', YOUTUBE_ID
        elif 'youtube' == self.pid:
            id_ind, desc_name, desc_ind = YOUTUBE_ID, 'DEEZER_ID', DEEZER_ID
        else:
            print('Given provider is not in DALI')
            return

        dir_path = dirname(realpath(__file__))
        with open(join(dir_path, 'DALI_deezer.json'), "r") as json_file:
            dali, c = Selection.objects.get_or_create(
                title=self.selection_title,
            )
            # skipping first line of columns descriptions
            data = json.load(json_file)[1:]
            if self.all:
                # loop over all DALI`s tracks
                indices = range(len(data))
            else:
                # generate 'n' unique random indices within DALI size
                indices = random.sample(range(len(data)), self.item_number)
            
            for i in indices:
                track = data[i]
                item, c = Item.objects.get_or_create(
                    external_id=track[id_ind],
                    title=track[NAME],
                    description=(f"DALI_ID: {track[DALI_ID]}\n"
                                 f"WASABI_ID: {track[WASABI_ID]}\n"
                                 f"{desc_name}: {track[desc_ind]}\n"
                                 f"WORKING: {track[WORKING]}"),
                    provider=Provider.objects.get(pid=self.pid)
                    )
                dali.items.add(item)
