#!/bin/bash

# uwsgi params
port=8000
processes=8
threads=8
autoreload=3

# uid / gid params for app and worker
uid='www-data'
gid='www-data'

# paths
app='/srv/app'
src='/srv/src'
static='/srv/static/'
media='/srv/media/'
log='/var/log/app'

# entrypoints
manage=$app'/manage.py'
wsgi=$app'/wsgi.py'

# levels
log_level='DEBUG'

# log paths
app_log_dir='/var/log/app'
app_log_file=$app_log_dir'/app.log'
worker_log_dir='/var/log/celery'
worker_log_file=$worker_log_dir'/worker.log'

# check and fix dirs
mkdir -p $app_log_dir
chown -R $uid:$gid $app_log_dir
mkdir -p $worker_log_dir
chown -R $uid:$gid $worker_log_dir
# mkdir -p $media
# chown -R $uid:$gid $media

# # FIXME install timeisde at start (pip bug on build)
# cd /srv/lib/timeside; pip3 install -e .

# install the last version of those packages
pip3 install -U youtube-dl

# Install plugins
bash /srv/app/bin/setup_plugins.sh

# fix media access rights
# find $media -maxdepth 1 -path ${media}import -prune -o -type d -not -user $uid -exec chown $uid:$gid {} \;
#chown -R $uid:$gid $media

# wait for other services
# bash $app/bin/wait.sh

#pip3 install librosa==0.7.2 numba==0.43.0

mkdir -p $NUMBA_CACHE_DIR
chown -R $uid:$gid $NUMBA_CACHE_DIR
