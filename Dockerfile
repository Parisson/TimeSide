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

FROM debian:jessie

MAINTAINER Guillaume Pellerin <yomguy@parisson.com>, Thomas fillon <thomas@parisson.com>

RUN mkdir /opt/TimeSide
WORKDIR /opt/TimeSide

# install confs, keys and deps
ADD debian-requirements.txt /opt/TimeSide/
RUN echo 'deb http://debian.parisson.com/debian/ jessie main' > /etc/apt/sources.list.d/parisson.list && \
    apt-get update && \
    DEBIAN_PACKAGES=$(egrep -v "^\s*(#|$)" /opt/TimeSide/debian-requirements.txt) && \
    apt-get install -y --force-yes $DEBIAN_PACKAGES && \
    apt-get install -y --force-yes python-yaafe && \
    apt-get install -y --force-yes git wget bzip2 build-essential netcat npm libmysqlclient-dev libxml2-dev libxslt1-dev && \
    apt-get clean

# Install conda in /opt/miniconda
ENV PATH /opt/miniconda/bin:$PATH
RUN wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/miniconda && \
    rm miniconda.sh && \
    hash -r && \
    conda config --set always_yes yes --set changeps1 yes && \
    conda update -q conda

# Install uwsgi
RUN conda install pip && \
    pip install uwsgi


# Install binary dependencies with conda
ADD conda-requirements.txt /opt/TimeSide/
#ADD requirements.txt /opt/TimeSide/
RUN conda install -c https://conda.anaconda.org/piem  --file conda-requirements.txt

# Link Yaafe in site-packages
RUN ln -s /usr/lib/python2.7/dist-packages/yaafelib /opt/miniconda/lib/python2.7

# Clone app
ADD . /opt/TimeSide
WORKDIR /opt/TimeSide

RUN pip install -r requirements.txt

RUN apt-get install -y --force-yes nodejs-legacy
RUN npm install -g bower

# install new deps from the local repo
#RUN pip install -e /opt/TimeSide

# add dev repo path
#RUN cd /opt/TimeSide; python setup.py develop

# Sandbox setup
# RUN /opt/TimeSide/examples/sandbox/manage.py syncdb --noinput && \
#     /opt/TimeSide/examples/sandbox/manage.py migrate --noinput && \
#     /opt/TimeSide/examples/sandbox/manage.py collectstatic --noinput

EXPOSE 8000
