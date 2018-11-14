from django.core.management.base import BaseCommand

from timeside.server.models import Item


class Command(BaseCommand):
    help = "This command will generate all post_save callback and will thus create audio_duration, mime_type and sha1 field if missing"

    def handle(self, *args, **options):
        for item in Item.objects.all():
            item.save()
