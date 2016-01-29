
Install
=======

Thanks to Docker, TimeSide is now fully available for every platform as a docker image ready to work. The image includes all the necessary applications, modules and volumes to start your project in a few seconds.

Just install, `Docker engine <https://docs.docker.com/installation/>`_ then pull the TimeSide image::

    docker pull parisson/timeside:latest

That's it! Now please go to the documentation to see how to use it.

For advanced usage (webserver, notebook, etc), you will also need `Git <http://git-scm.com/downloads>`_ and `docker-compose <https://docs.docker.com/compose/install/>`_.

.. note :: If you need to user TimeSide outside a docker image please refer to the rules of the Dockerfile which is based on a Debian stable system. But we do not provide any kind of free support in this usercase anymore (the dependency list is now huge). To get commercial support in more various usecases, please reach the Parisson dev team.
