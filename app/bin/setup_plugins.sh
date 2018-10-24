#!/bin/bash

plugins=/srv/lib/plugins

for dir in $(ls $plugins); do
    
    env=$plugins/$dir/conda-environment.yml
    if [ -f $env ]; then
        conda env update --name root --file $env
    fi
    
    req=$plugins/$dir/debian-requirements.txt
    if [ -f $req ]; then
        apt-get update
        packs=$(egrep -v "^\s*(#|$)" $req)
        apt-get install -y --force-yes $packs
        apt-get clean
    fi
    
    if [ -f $plugins/$dir/setup.py ]; then
        pip install -e $plugins/$dir/.
    fi

done


