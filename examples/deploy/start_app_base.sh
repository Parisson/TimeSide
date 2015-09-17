#!/bin/bash

# paths
app_dir='/opt/TimeSide'
sandbox='/home/sandbox'
manage=$sandbox'/manage.py'
wsgi=$sandbox'/wsgi.py'

# stating apps
pip install django-bootstrap3 elasticsearch django-angular django-bower django-bootstrap-pagination

sh $app_dir/examples/deploy/wait.sh
