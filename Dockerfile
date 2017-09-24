# Copyright 2013 Thatcher Peskens
# Copyright 2015, 2016 Guillaume Pellerin, Thomas Fillon
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

FROM parisson/docker:v0.4

MAINTAINER Guillaume Pellerin <yomguy@parisson.com>, Thomas fillon <thomas@parisson.com>

RUN mkdir -p /srv/app
RUN mkdir -p /srv/src
RUN mkdir -p /srv/src/timeside
WORKDIR /srv/src/timeside

# install confs, keys and deps
COPY debian-requirements.txt /srv/src/timeside/
RUN apt-get update && \
    DEBIAN_PACKAGES=$(egrep -v "^\s*(#|$)" debian-requirements.txt) && \
    apt-get install -y --force-yes $DEBIAN_PACKAGES && \
    apt-get clean

# Install binary dependencies with conda
COPY environment-pinned.yml /srv/src/timeside/
RUN conda update conda &&\
    conda config --append channels conda-forge --append channels thomasfillon &&\
    conda env update --name root --file environment-pinned.yml &&\
    pip install -U --force-reinstall functools32 &&\              
    conda clean --all --yes

# Link glib-networking with Conda to fix missing TLS/SSL support in Conda Glib library
RUN rm /opt/miniconda/lib/libgio* &&\
    ln -s /usr/lib/x86_64-linux-gnu/libgio* /opt/miniconda/lib/

COPY . /srv/src/timeside/

ENV PYTHON_EGG_CACHE=/srv/.python-eggs
RUN mkdir -p $PYTHON_EGG_CACHE
RUN chown www-data:www-data $PYTHON_EGG_CACHE

# Install TimeSide
RUN pip install -e .

# Install Timeside plugins from ./lib
COPY ./app/bin/setup_plugins.sh /srv/app/bin/setup_plugins.sh
COPY ./lib/ /srv/src/plugins/
RUN /bin/bash /srv/app/bin/setup_plugins.sh

# Install Vamp plugins
COPY ./app/bin/install_vamp_plugins.sh /srv/app/bin/install_vamp_plugins.sh
RUN /bin/bash /srv/app/bin/install_vamp_plugins.sh

WORKDIR /srv/app
EXPOSE 8000
