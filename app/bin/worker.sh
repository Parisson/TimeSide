#!/bin/bash

SCRIPT_DIR="$(dirname "$0")"
source "$SCRIPT_DIR/app_base.sh"

# Starting celery worker with the --autoreload option will enable the worker to watch for file system changes
# This is an experimental feature intended for use in development only
# see http://celery.readthedocs.org/en/latest/userguide/workers.html#autoreloading

# python $manage celery worker -A worker --uid $uid --gid $gid
celery -A worker worker --logfile=$worker_log
