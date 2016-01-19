#!/bin/bash

# paths
app='/srv/app'
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
#pip install django-bootstrap3 elasticsearch django-angular django-bower django-bootstrap-pagination Werkzeug

chown $uid:$gid $media

# wait for other services
bash $app/deploy/wait.sh
