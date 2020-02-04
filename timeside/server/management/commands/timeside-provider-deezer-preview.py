from django.core.management.base import BaseCommand

from timeside.server.models import Item
from timeside.server.models import Provider

import timeside.core


class Command(BaseCommand):
    help = "                                                                \
    Switch all Items with deezer as Provider ForeignKey field to            \
    deezer_preview. Delete deprecated deezer provider.                      \
    Check and clean server providers on database.                           \
    "

    def handle(self, *args, **options):
        server_prodivers = {}
        core_providers = timeside.core.provider.providers(
            timeside.core.api.IProvider
            )
        for prov in core_providers:
            provider, c = Provider.objects.get_or_create(
                pid=prov.id(),
                source_access=prov.ressource_access(),
                name=prov.name()
                )
            server_prodivers[prov.id()] = provider
        for item in Item.objects.all():
            if item.provider and                             \
               item.provider not in server_prodivers.values():
                # Switch items with deezer as to deezer_preview
                if item.provider.pid == "deezer":
                    item.provider = server_prodivers['deezer_preview']
                # Switch item's provider foreignkeys to duplicated providers
                else:
                    item.provider = server_prodivers[item.provider.pid]
                item.save()
        for prov in Provider.objects.all():
            # Delete duplicated providers and old 'deezer' provider
            if prov not in server_prodivers.values():
                prov.delete()
