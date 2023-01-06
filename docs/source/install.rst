
Install
=======

Thanks to Docker, Timeside is now fully available as a docker composition ready to work. The docker based composition bundles some powerfull applications and modern frameworks out-of-the-box like: Python, Conda, Numpy, Jupyter, Gstreamer, Django, Celery, Haystack, ElasticSearch, MySQL, Redis, uWSGI, Nginx and many more.

First, install `Docker <https://docs.docker.com/get-docker/>`_ and `docker-compose <https://docs.docker.com/compose/install/>`_

Then clone TimeSide and start it up::

    git clone --recursive https://github.com/Ircam-WAM/TimeSide.git
    cd TimeSide
    docker-compose up -d

That's it! Now please go to the User Interfaces section to see how to use it.

.. note::
   To get technical support, please reach the development team. If you need to use TimeSide *outside* a docker image please refer to the rules of the Dockerfile which is based on a Debian stable system. But we do not provide any kind of free support in this "third party" usecase anymore.
