#!/bin/bash

plugins=/srv/src/plugins

apt-get update

for dir in $(ls $plugins); do
    env=$plugins/$dir/conda-environment.yml
    if [ -f $env ]; then
        conda env update --name root --file $env
    fi
    req=$plugins/$dir/debian-requirements.txt
    if [ -f $req ]; then
        packs=$(egrep -v "^\s*(#|$)" $req)
        apt-get install -y --force-yes $packs
    fi
    if [ -f $plugins/$dir/setup.py ]; then
        pip install -e $plugins/$dir/.
    fi
done

apt-get clean
