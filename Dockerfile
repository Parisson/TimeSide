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

FROM parisson/docker

MAINTAINER Guillaume Pellerin <yomguy@parisson.com>, Thomas fillon <thomas@parisson.com>

RUN mkdir /srv/app
RUN mkdir /srv/src
RUN mkdir /srv/src/timeside
WORKDIR /srv/src/timeside

# install confs, keys and deps
COPY debian-requirements.txt /srv/src/timeside/
RUN apt-get update && \
    DEBIAN_PACKAGES=$(egrep -v "^\s*(#|$)" debian-requirements.txt) && \
    apt-get install -y --force-yes $DEBIAN_PACKAGES && \
    apt-get clean

# Install binary dependencies with conda
COPY environment-pinned.yml /srv/src/timeside/
RUN conda config --add channels piem &&\
    conda env update --name root --file environment-pinned.yml

COPY . /srv/src/timeside/

ENV PYTHON_EGG_CACHE=/srv/.python-eggs
RUN mkdir $PYTHON_EGG_CACHE
RUN chown www-data:www-data $PYTHON_EGG_CACHE

# Install TimeSide
RUN pip install -e .

WORKDIR /srv/app
EXPOSE 8000
