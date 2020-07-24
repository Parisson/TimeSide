#!/bin/bash
set -e

cd app
./manage.py syncdb --noinput
./manage.py migrate
./manage.py runserver &
TESTPID=$! 
sleep 20
kill -2 $TESTPID
