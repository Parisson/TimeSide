from django.core.management.base import BaseCommand

from timeside.server.models import (
    Item,
    Provider,
    Selection,
    Experience,
)

import timeside.core
import json
from os.path import join
import sys

# DALI columns descriptions
DALI_ID, WASABI_ID, NAME, DEEZER_ID, YOUTUBE, WORKING = 0, 1, 2, 3, 4, 5


class Command(BaseCommand):
    help = """
    Create an Item for all DALI's tracks
    with deezer_complete provider
    """

    def handle(self, *args, **options):
        with open(join(sys.path[0], 'DALI_deezer.json'), "r") as json_file:
            dali, c = Selection.objects.get_or_create(
                title="DALI_corpus",
                # items=[],
                # selections=[],
            )
            # skipping first line of columns descriptions
            data = json.load(json_file)[1:]
            for track in data:
                item, c = Item.objects.get_or_create(
                    external_id=track[DEEZER_ID],
                    title=track[NAME],
                    description=(f"DALI_ID: {track[DALI_ID]}\n"
                                 f"WASABI_ID: {track[WASABI_ID]}\n"
                                 f"YOUTUBE_ID: {track[YOUTUBE]}\n"
                                 f"WORKING: {track[WORKING]}"),
                    provider=Provider.objects.get(pid='deezer_complete')                    
                    )
                dali.items.add(item)
