# Copyright 2013 Thatcher Peskens
# Copyright 2014 Guillaume Pellerin
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from debian:stable

maintainer Guillaume Pellerin <yomguy@parisson.com>

add ./deploy/apt-app.list /etc/apt/sources.list.d/
run apt-get update
run apt-get install -y --force-yes build-essential vim
run apt-get install -y python python-dev python-pip
run apt-get -y -t wheezy-backports dist-upgrade
run apt-get install -y --force-yes -t wheezy-backports nginx supervisor python-timeside git python-tables python-django python-traits python-networkx ipython
run apt-get clean

# install uwsgi now because it takes a little while
run pip install uwsgi ipython

# clone app
add . /opt/TimeSide

# setup all the configfiles
run echo "daemon off;" >> /etc/nginx/nginx.conf
run rm /etc/nginx/sites-enabled/default
run ln -s /opt/TimeSide/deploy/nginx-app.conf /etc/nginx/sites-enabled/
run ln -s /opt/TimeSide/deploy/supervisor-app.conf /etc/supervisor/conf.d/

# run pip install
run pip install -e /opt/TimeSide

# sandbox setup
run /opt/TimeSide/examples/sandbox/manage.py syncdb --noinput
run /opt/TimeSide/examples/sandbox/manage.py migrate --noinput
run /opt/TimeSide/examples/sandbox/manage.py collectstatic --noinput

expose 80
cmd ["supervisord", "-n"]
