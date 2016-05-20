#!/bin/bash

# paths
app='/srv/app'
src='/srv/src'
manage=$app'/manage.py'
wsgi=$app'/wsgi.py'
static='/srv/static/'
media='/srv/media/'

# uwsgi params
port=8000
processes=8
threads=8
autoreload=3
uid='www-data'
gid='www-data'

# staging apps
pip install django-cors-headers

# wait for other services
bash $app/scripts/wait.sh
