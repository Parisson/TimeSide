
Development
===========

|travis_dev| |coveralls_dev|

.. |travis_dev| image:: https://travis-ci.org/Parisson/TimeSide.svg?branch=dev
    :target: https://travis-ci.org/Parisson/TimeSide/

.. |coveralls_dev| image:: https://coveralls.io/repos/Parisson/TimeSide/badge.png?branch=dev
  :target: https://coveralls.io/r/Parisson/TimeSide?branch=dev

Developing within TimeSide
--------------------------

If the TimeSide library gives you everything you need to develop you own plugin, it is advised to start with one existing. For example, starting from the DC analyzer::

    git clone https://github.com/Parisson/TimeSide.git
    cd TimeSide
    git checkout dev
    cp timeside/plugins/analyzer/dc.py timeside/plugins/analyzer/my_analyzer.py

Before coding, start docker with mounting the local directory as a volume::

    docker run -it -v .:/srv/src/timeside parisson/timeside:latest ipython

or use the development composition to start a notebook or the webserver::

    docker-compose -f docker-compose.yml -f conf/dev.yml up

Developing your own external plugins
------------------------------------

If the (already huge) python module bundle provided by TimeSide is to short for you, it is possible to make your own plugin bundle outside the core module thanks to the TimeSide namespace. An extensive example of what you can do is available in the `DIADEMS project repository <https://github.com/ANR-DIADEMS/timeside-diadems/>`_. You can also start with the dummy plugin::

    git clone https://github.com/Parisson/TimeSide-Dummy.git
    cd TimeSide-Dummy
    docker run -it -v ./timeside/plugins/:/srv/src/timeside/timeside/plugins parisson/timeside:latest ipython

or::

    docker-compose -f docker-compose.yml -f conf/dummy.yml up
