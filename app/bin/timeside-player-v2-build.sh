#/bin/bash

npm install -g bower
npm install -g grunt-cli
apt install -y ruby-sass

cd /srv/lib/timeside/timeside/player/static/timeside2

bower install --allow-root
grunt build --force
