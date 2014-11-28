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

# install confs, keys and deps
run gpg --keyserver pgpkeys.mit.edu --recv-key E3298399DF14BB7C
run gpg -a --export E3298399DF14BB7C | apt-key add -
run gpg --keyserver pgpkeys.mit.edu --recv-key 07DC563D1F41B907
run gpg -a --export 07DC563D1F41B907 | apt-key add -
add ./deploy/apt-app.list /etc/apt/sources.list.d/
run apt-get update
run apt-get install -y --force-yes apt-utils
run apt-get -y --force-yes -t wheezy-backports dist-upgrade
run apt-get install -y --force-yes -t wheezy-backports build-essential vim python python-dev python-pip nginx postgresql python-psycopg2 supervisor python-timeside git python-tables python-traits python-networkx ipython python-numexpr gstreamer0.10-alsa
run apt-get clean

# install tools via pip
run pip install uwsgi ipython

# clone app
add . /opt/TimeSide

# setup all the configfiles
run echo "daemon off;" >> /etc/nginx/nginx.conf
run rm /etc/nginx/sites-enabled/default
run ln -s /opt/TimeSide/deploy/nginx-app.conf /etc/nginx/sites-enabled/
run ln -s /opt/TimeSide/deploy/supervisor-app.conf /etc/supervisor/conf.d/

# install new deps from the local repo
run pip install -e /opt/TimeSide

# add dev repo path
run echo "export PYTHONPATH=$PYTHONPATH:/opt/Timeside" >> ~/.bashrc

# sandbox setup
run /opt/TimeSide/examples/sandbox/manage.py syncdb --noinput
run /opt/TimeSide/examples/sandbox/manage.py migrate --noinput
run /opt/TimeSide/examples/sandbox/manage.py collectstatic --noinput

expose 80
cmd ["supervisord", "-n"]
