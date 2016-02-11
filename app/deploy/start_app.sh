#!/bin/bash

SCRIPT_DIR="$(dirname "$0")"
source "$SCRIPT_DIR/start_app_base.sh"

# django init
python $manage migrate --noinput
python $manage bower_install -- --allow-root
python $manage collectstatic --noinput

python $manage timeside-create-admin-user
python $manage timeside-create-boilerplate


# static files auto update
watchmedo shell-command --patterns="*.js;*.css" --recursive \
    --command='python '$manage' collectstatic --noinput' $src &

# app start
if [ $1 == "--runserver" ]
then
    python $manage runserver_plus 0.0.0.0:8000
else
    uwsgi --socket :$port --wsgi-file $wsgi --chdir $app --master \
        --processes $processes --threads $threads \
        --uid $uid --gid $gid \
        --py-autoreload $autoreload
fi
