
Development
===========

|travis_dev| |coveralls_dev|

.. |travis_dev| image:: https://secure.travis-ci.org/Parisson/TimeSide.png?branch=dev
    :target: https://travis-ci.org/Parisson/TimeSide/

.. |coveralls_dev| image:: https://coveralls.io/repos/Parisson/TimeSide/badge.png?branch=dev
  :target: https://coveralls.io/r/Parisson/TimeSide?branch=dev


Developing in TimeSide Core
----------------------------

Just use the development composition in the dev branch::

    git clone https://github.com/Parisson/TimeSide.git
    cd TimeSide
    git checkout dev
    docker-compose -f docker-compose.yml -f conf/dev.yml up


Developing your own plugins
----------------------------

TimeSide is using a namespace so you can develop your own plugins outside the core module. Then, adding your module to the PYTHONPATH will automatically import your plugins within TimeSide. An example of what you can do is available in the `DIADEMS project repository <https://github.com/ANR-DIADEMS/timeside-diadems/>`_.

Clone the dummy plugin repository inside the TimeSide directory and use the dummy development composition::

    git clone https://github.com/Parisson/TimeSide.git
    cd TimeSide
    git clone https://github.com/Parisson/timeside-dummy.git
    docker-compose -f docker-compose.yml -f conf/dev-dummy.yml up


Build your own image
---------------------

You can also re-build your own image locally::

    docker-compose -f docker-compose.yml conf/dev-build.yml up
