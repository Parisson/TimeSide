#!/bin/bash

SCRIPT_DIR="$(dirname "$0")"
source "$SCRIPT_DIR/app_base.sh"

if [ $DEBUG = True ]; then
    python3 manage.py timeside-celery-worker --loglevel $loglevel --logfile $worker_logfile --uid $uid --gid $gid
else
<<<<<<< HEAD
    celery -A worker worker --loglevel=$loglevel --logfile=$worker_logfile --uid $uid --gid $gid
=======
    celery -A worker worker --loglevel=$loglevel --logfile=$worker_logfile --uid=$uid --gid=$gid
>>>>>>> [server] add uid and gid args to celery worker command
fi

