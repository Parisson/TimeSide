#!/bin/bash

SCRIPT_DIR="$(dirname "$0")"
source "$SCRIPT_DIR/start_app_base.sh"


# django init
python $manage syncdb --noinput
python $manage migrate --noinput
python $manage bower_install -- --allow-root
python $manage collectstatic --noinput
python $manage timeside-create-admin-user
python $manage timeside-create-boilerplate

# static files auto update
watchmedo shell-command --patterns="*.js;*.css" --recursive \
    --command='python '$manage' collectstatic --noinput' $static &

# app start
uwsgi --socket :8000 --wsgi-file $wsgi --chdir $sandbox --master --processes 4 --threads 2 --py-autoreload 3
