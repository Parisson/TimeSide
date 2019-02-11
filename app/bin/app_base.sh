#!/bin/bash

# paths
app='/srv/app'
src='/srv/src'
manage=$app'/manage.py'
wsgi=$app'/wsgi.py'
static='/srv/static/'
media='/srv/media/'
log='/var/log/uwsgi/app.log'

# uwsgi params
port=8000
processes=4
threads=4
autoreload=3
uid='www-data'
gid='www-data'

# staging apps
# pip install -U django-cors-headers
# pip install django-debug-toolbar
# pip install jsonfield
# pip uninstall -y mysql-python
# pip install -U mysql-python django==1.10.8 djangorestframework==3.8.2 mysqlclient
pip install coreapi

# Install plugins
bash /srv/app/bin/setup_plugins.sh

# wait for other services
bash $app/bin/wait.sh
