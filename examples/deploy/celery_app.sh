#!/bin/sh

# paths
app_dir='/opt/TimeSide/'
sandbox_dir='/home/timeside/'
manage=$sandbox_dir'manage.py'

# cp -uR /opt/TimeSide/examples/sandbox/* /home/timeside/

echo "YYYYYYYYYYYYYY"

pip install django-celery

python $manage migrate --noinput

# run Celery worker for our project myproject with Celery configuration stored in Celeryconf
su -c "$manage celery worker -A celery_app"
