#!/bin/sh

# paths
app_dir='/opt/TimeSide'
static=$app_dir'/timeside/player/static/'
sandbox='/home/sandbox'
manage=$sandbox'/manage.py'
wsgi=$sandbox'/wsgi.py'

sh $app_dir/examples/deploy/wait.sh

# django init
python $manage syncdb --noinput
python $manage migrate --noinput
python $manage bower install
python $manage collectstatic --noinput
python $manage timeside-create-admin-user
python $manage timeside-create-boilerplate

# static files auto update
watchmedo shell-command --patterns="*.js;*.css" --recursive \
    --command='python '$manage' collectstatic --noinput' $static &

# app start
uwsgi --socket :8000 --wsgi-file $wsgi --chdir $sandbox --master --processes 4 --threads 2 --py-autoreload 3
