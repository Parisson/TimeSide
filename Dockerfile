# Copyright 2013 Thatcher Peskens
# Copyright 2015, 2017 Guillaume Pellerin, Thomas Fillon
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

FROM debian:buster

MAINTAINER Guillaume Pellerin <guillaume.pellerin@ircam.fr>

RUN mkdir -p /srv/lib
RUN mkdir -p /srv/lib/timeside

WORKDIR /srv/lib

# install confs, keys and deps
RUN apt-get update && apt-get install -y apt-transport-https
COPY requirements-debian.txt /srv/lib/
RUN apt-get update && \
    DEBIAN_PACKAGES=$(egrep -v "^\s*(#|$)" requirements-debian.txt) && \
    apt-get install -y --force-yes $DEBIAN_PACKAGES && \
    apt-get clean

ENV PYTHON_EGG_CACHE=/srv/.python-eggs
RUN mkdir -p $PYTHON_EGG_CACHE && \
    chown www-data:www-data $PYTHON_EGG_CACHE

RUN pip3 install -U setuptools pip numpy
RUN apt-get remove -y python3-yaml

# Install timeside
WORKDIR /srv/lib/timeside
COPY ./requirements.txt /srv/lib/timeside/
RUN pip3 install -r requirements.txt

# Install app
COPY ./app /srv/app

# Install Timeside plugins from ./lib
RUN mkdir -p /srv/lib/plugins
COPY ./lib/plugins/ /srv/lib/plugins/
RUN /bin/bash /srv/app/bin/setup_plugins.sh

# Link python gstreamer
RUN python3 /srv/app/bin/link_gstreamer.py

# Install Vamp plugins
RUN /bin/bash /srv/app/bin/install_vamp_plugins.sh

COPY ./README.rst /srv/lib/timeside/
COPY ./LICENSE.txt /srv/lib/timeside/
COPY ./setup.py /srv/lib/timeside/
COPY ./docs /srv/lib/timeside/docs/
COPY ./tests /srv/lib/timeside/tests/
COPY ./bin /srv/lib/timeside/bin/
COPY ./timeside /srv/lib/timeside/timeside/
RUN pip3 install -e .

RUN export PYTHONPATH=/srv/lib/timeside:/srv/app

WORKDIR /srv/app

