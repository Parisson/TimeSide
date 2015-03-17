Development
===========

|travis_dev| |coveralls_dev|

.. |travis_dev| image:: https://secure.travis-ci.org/Parisson/TimeSide.png?branch=dev
    :target: https://travis-ci.org/Parisson/TimeSide/

.. |coveralls_dev| image:: https://coveralls.io/repos/Parisson/TimeSide/badge.png?branch=dev
  :target: https://coveralls.io/r/Parisson/TimeSide?branch=dev


Docker (recommended)
--------------------

Docker is a great tool for developing and deploying processing environments. We provide a docker image which contains TimeSide and all the necessary packages (nginx, uwsgi, etc) to run it either in development or in production stages.

First, install Docker: https://docs.docker.com/installation/

Then, simply pull the image and run it::

  docker pull parisson/timeside
  docker run -p 9000:80 parisson/timeside

You can now browse the TimeSide API: http://localhost:9000/api/

or get a shell session::

  docker run -ti parisson/timeside bash

To start a new development, it is advised to checkout the dev branch in the container::

  cd /opt/TimeSide
  git checkout dev

or get our latest-dev image::

  docker pull parisson/timeside:latest-dev

More infos: https://registry.hub.docker.com/u/parisson/timeside/


Native
-------

First, install TimeSide (see Install).

Then::

 sudo apt-get build-dep python-timeside
 sudo apt-get install git
 git clone https://github.com/Parisson/TimeSide.git
 cd TimeSide
 git checkout dev
 sudo pip install -e .
 echo "export PYTHONPATH=$PYTHONPATH:`pwd`" >> ~/.bashrc
 source ~/.bashrc
 tests/run_all_tests


