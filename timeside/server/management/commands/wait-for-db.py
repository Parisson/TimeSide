import os, time

from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connections


class Command(BaseCommand):
    help = "wait for default DB connection"

    db_name = 'default'
    N = 10

    def handle(self, *args, **options):
        i = 0
        connected = False
        db_conn = connections[self.db_name]
        while not connected:
            try:
                c = db_conn.cursor()
                connected = True
            except:
                print('error connecting to DB...')
                if i > self.N:
                    print('...exiting')
                    raise
                print('...retrying')
                i += 1
                time.sleep(1)
