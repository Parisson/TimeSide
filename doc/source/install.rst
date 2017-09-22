
Install
=======

Thanks to Docker, Telemeta is now fully available as a docker composition ready to work. The docker based composition bundles somThanks to Docker, Telemeta is now fully available as a docker composition ready to work. The docker based composition bundles some powerfull applications and modern frameworks out-of-the-box like: Python, Conda, Numpy, Jupyter, Gstreamer, Django, Celery, Haystack, ElasticSearch, MySQL, Redis, uWSGI, Nginx and many more.

First, install `Docker <https://store.docker.com/search?offering=community&q=&type=edition>`_ and `docker-compose <https://docs.docker.com/compose/>`_

Then clone TimeSide::

    git clone --recursive https://github.com/Parisson/TimeSide.git
    cd TimeSide
    docker-compose build

That's it! Now please go to the documentation to see how to use it.

.. note :: If you need to user TimeSide outside a docker image please refer to the rules of the Dockerfile which is based on a Debian stable system. But we do not provide any kind of free support in this usercase anymore (the dependency list is now huge). To get commercial support in more various usecases, please reach the Parisson dev team.
