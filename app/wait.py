#!/usr/bin/python

import os, time
from django.core.management import call_command

up = False
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

while not up:
    try:
        call_command('syncdb', interactive=False)
        up = True
    except:
        time.sleep(1)
