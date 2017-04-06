#!/bin/sh

./manage.py schemamigration timeside.server --auto
./manage.py migrate timeside.server

