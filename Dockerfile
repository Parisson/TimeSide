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

FROM debian:jessie

MAINTAINER Guillaume Pellerin <yomguy@parisson.com>, Thomas fillon <thomas@parisson.com>

RUN mkdir -p /srv/app
RUN mkdir -p /srv/lib
RUN mkdir -p /srv/lib/timeside

WORKDIR /srv/lib

# install confs, keys and deps
COPY ./etc/apt/sources.list /etc/apt/
RUN apt-get update && apt-get install -y apt-transport-https
COPY debian-requirements.txt /srv/lib/
RUN apt-get update && \
    DEBIAN_PACKAGES=$(egrep -v "^\s*(#|$)" debian-requirements.txt) && \
    apt-get install -y --force-yes $DEBIAN_PACKAGES && \
    apt-get clean

# Install conda in /opt/miniconda
ENV PATH /opt/miniconda/bin:$PATH
RUN wget https://repo.anaconda.com/miniconda/Miniconda2-latest-Linux-x86_64.sh -O miniconda.sh && \
    /bin/bash miniconda.sh -b -p /opt/miniconda && \
    rm miniconda.sh && \
    hash -r && \
    ln -s /opt/miniconda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/miniconda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate" >> ~/.bashrc && \
    conda config --set always_yes yes --set changeps1 yes

#COPY environment-pinned.yml /srv/lib/
COPY environment-explicit.yml /srv/lib/
RUN conda config --append channels conda-forge --append channels thomasfillon --append channels soumith &&\
     #conda env update --file environment-pinned.yml &&\
     conda install -n base --file environment-explicit.yml &&\
    conda clean --all --yes

# Link glib-networking with Conda to fix missing TLS/SSL support in Conda Glib library
#RUN rm /opt/miniconda/lib/libgio* &&\
#    ln -s /usr/lib/x86_64-linux-gnu/libgio* /opt/miniconda/lib/

ENV PYTHON_EGG_CACHE=/srv/.python-eggs
RUN mkdir -p $PYTHON_EGG_CACHE && \
    chown www-data:www-data $PYTHON_EGG_CACHE

# Link python gstreamer
RUN mkdir -p /srv/app/bin
COPY ./app/bin/link_gstreamer.py /srv/app/bin/
RUN python /srv/app/bin/link_gstreamer.py

# Install Timeside plugins from ./lib
RUN mkdir -p /srv/lib/plugins
COPY ./lib/plugins/ /srv/lib/plugins/
COPY ./app/bin/setup_plugins.sh /srv/app/bin/
RUN /bin/bash /srv/app/bin/setup_plugins.sh

# Install Vamp plugins
COPY ./app/bin/install_vamp_plugins.sh /srv/app/bin/
RUN /bin/bash /srv/app/bin/install_vamp_plugins.sh

# Install bower
RUN npm install -g bower

# Install timeside
WORKDIR /srv/lib/timeside
COPY . /srv/lib/timeside/
RUN pip install -U pip
RUN pip install -e .

WORKDIR /srv/app
