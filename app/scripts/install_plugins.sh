#!/bin/bash

plugins=/srv/src/plugins

for dir in $(ls $plugins); do
    if [ -f $plugins/$dir/setup.py ]; then
        pip install -e $plugins/$dir/.
    fi
done
