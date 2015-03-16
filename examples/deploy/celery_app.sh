#!/bin/sh

# paths
app_dir='/opt/TimeSide/'
sandbox_dir='/home/timeside/'
manage=$sandbox_dir'manage.py'

python $manage migrate --noinput

$manage celery worker -A celery_app
