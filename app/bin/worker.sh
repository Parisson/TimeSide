#!/bin/bash

SCRIPT_DIR="$(dirname "$0")"
source "$SCRIPT_DIR/app_base.sh"

python3 manage.py timeside-celery-worker --loglevel $log_level --logfile $worker_log_file --uid $uid --gid $gid

