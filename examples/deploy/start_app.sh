#!/bin/sh

# paths
app_dir='/opt/TimeSide/'
sandbox_dir='/home/timeside/'
manage=$sandbox_dir'manage.py'
wsgi=$sandbox_dir'wsgi.py'
app_static_dir=$app_dir'timeside/player/static/'

# Copy Sandbox in /home/timeside
#  this is not needed for TimeSide but for Timeside-diadems
# cp -uR /opt/TimeSide/examples/sandbox/* /home/timeside/

# install staging modules
pip install mysql

# django init
python $manage syncdb --noinput
python $manage migrate --noinput
python $manage collectstatic --noinput
python $manage timeside-create-admin-user

# static files auto update
watchmedo shell-command --patterns="*.js;*.css" --recursive \
    --command='python '$manage' collectstatic --noinput' $app_static_dir &

# app start
uwsgi --socket :8000 --wsgi-file $wsgi --chdir $sandbox_dir --master --processes 4 --threads 2 --py-autoreload 3
