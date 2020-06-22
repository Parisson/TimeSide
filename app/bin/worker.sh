#!/bin/bash

SCRIPT_DIR="$(dirname "$0")"
source "$SCRIPT_DIR/app_base.sh"

# fix celery log access
mkdir -p '/var/log/celery/'
chown -R $uid:$gid '/var/log/celery/'

python3 manage.py timeside-celery-worker --loglevel $loglevel --logfile $worker_logfile --uid $uid --gid $gid

