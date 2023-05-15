#!/bin/bash

SCRIPT_DIR="$(dirname "$0")"
source "$SCRIPT_DIR/app_base.sh"

uid=www-data
gid=www-data

# waiting for db
python3 $manage wait-for-db

# run migrations
python3 $manage migrate --noinput

# timeside setup
python3 $manage timeside-create-admin-user
python3 $manage timeside-create-boilerplate
# su $uid -g $gid -s /bin/bash -c "python3 $manage timeside-analysis-subprocessor-quickfix"

# if [ $DEBUG = "False" ]; then
#     python $manage update_index --workers $processes &
# fi

# app start
if [ "$1" = "--runserver" ]
then
    su $uid -g $gid -s /bin/bash -c "python3 $manage runserver 0.0.0.0:8000"
else
    # fix static access
    chown -R $uid:$gid $static

    # collect static files
    su $uid -g $gid -s /bin/bash -c "python3 $manage collectstatic --noinput"

    # watchmedo shell-command --patterns="*.js;*.css" --recursive \
    #     --command='python '$manage' collectstatic --noinput' $src &

    uwsgi /srv/app/wsgi.ini
fi
