#!/bin/bash

SCRIPT_DIR="$(dirname "$0")"
echo $SCRIPT_DIR
source "$SCRIPT_DIR/start_app_base.sh"


# Starting celery worker with the --autoreload option will enable the worker to watch for file system changes
# This is an experimental feature intended for use in development only
# see http://celery.readthedocs.org/en/latest/userguide/workers.html#autoreloading
$manage celery worker --autoreload -A celery_app
