from django.core.management.base import BaseCommand

from timeside.server.models import Item


class Command(BaseCommand):
    help = """
    Save all Items to populate external id, sha1,
    mime type, samplerate and audio duration
    """

    def handle(self, *args, **options):
        for item in Item.objects.all():
            item.save()
