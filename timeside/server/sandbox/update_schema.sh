#!/bin/sh

./manage.py schemamigration timeside --auto
./manage.py migrate timeside

