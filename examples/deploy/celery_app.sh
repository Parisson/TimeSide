#!/bin/sh

# paths
app_dir='/opt/TimeSide/'
sandbox_dir='/home/timeside/'
manage=$sandbox_dir'manage.py'

pip install django-celery

python $manage migrate --noinput

# run Celery worker for our project myproject with Celery configuration stored in Celeryconf
$manage celery worker -A celery_app
