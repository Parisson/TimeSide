#!/bin/bash

SCRIPT_DIR="$(dirname "$0")"
source "$SCRIPT_DIR/app_base.sh"

# waiting for db
python3 $manage wait-for-db

# run migrations
python3 $manage migrate --noinput

# timeside setup
python3 $manage timeside-create-admin-user
python3 $manage timeside-create-boilerplate

# if [ $DEBUG = "False" ]; then
#     python $manage update_index --workers $processes &
# fi


# NPM modules install
npm install --prefix /srv/app


# app start
if [ "$1" = "--runserver" ]
then
    python3 $manage runserver 0.0.0.0:8000
else
    # static files auto update
    python3 $manage collectstatic --noinput

    # fix media access rights
    find $media -maxdepth 1 -path ${media}import -prune -o -type d -not -user www-data -exec chown www-data:www-data {} \;

    # watchmedo shell-command --patterns="*.js;*.css" --recursive \
    #     --command='python '$manage' collectstatic --noinput' $src &

    uwsgi --socket :$port --wsgi-file $wsgi --chdir $app --master \
        --processes $processes --threads $threads \
        --uid $uid --gid $gid --logto $log --touch-reload $wsgi
fi
