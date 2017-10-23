#!/bin/bash

SCRIPT_DIR="$(dirname "$0")"
source "$SCRIPT_DIR/app_base.sh"

# django init
python $manage wait-for-db
python $manage migrate --noinput
python $manage bower_install -- --allow-root

# timeside setup
python $manage timeside-create-admin-user
python $manage timeside-create-boilerplate

# fix media access rights
chown www-data:www-data $media
find $media -type d -exec chown www-data:www-data {} \;

if [ $DEBUG = "False" ]; then
    python $manage update_index --workers $processes &
fi

# app start
if [ "$1" = "--runserver" ]
then
    python $manage runserver 0.0.0.0:8000
else
    # static files auto update
    python $manage collectstatic --noinput -i *node_modules*

    # fix media access rights
    find $media -maxdepth 1 -path ${media}import -prune -o -type d -not -user www-data -exec chown www-data:www-data {} \;

    # watchmedo shell-command --patterns="*.js;*.css" --recursive \
    #     --command='python '$manage' collectstatic --noinput' $src &

    uwsgi --socket :$port --wsgi-file $wsgi --chdir $app --master \
        --processes $processes --threads $threads \
        --uid $uid --gid $gid \
        --py-autoreload $autoreload
fi
