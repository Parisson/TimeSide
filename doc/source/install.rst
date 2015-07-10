
Install
=======

Any platform - *with Docker*
-----------------------------

Thanks to Docker, TimeSide is now fully available as a docker image ready to work. The image includes all the necessary applications, modules and volumes to start your project in a few minutes.

First install `Docker <https://docs.docker.com/installation/>`_ then just pull our latest master image::

    docker pull parisson/timeside:latest

and then run the docker container as an interactive shell::

    docker run -it --name timeside -v $(pwd):/home/timeside parisson/timeside:latest /bin/bash

In this shell, you have access to `python` and `ipython` to play with TimeSide. And you have access to the current working directory inside the container in the /home/timeside directory.


Debian, Ubuntu
---------------

For Debian based distributions, we provide a safe public repository giving all additional binary dependencies that are not included in Debian yet. They ensure TimeSide to be installed natively although the setup is not trivial. Please follow the instructions on `this page <http://debian.parisson.com/debian/>`_ and the old NOT up to date install howto.


Advanced (and experimental) usage
----------------------------------

TimeSide now includes an experimental web service and API. To test this new environnement please install  `Git <http://git-scm.com/downloads>`_ and `docker-compose <https://docs.docker.com/compose/install/>`_, then copy these commands in a terminal and hit ENTER::

    git clone https://github.com/Parisson/TimeSide.git
    cd TimeSide
    docker-compose up

That's it! You can now browse the TimeSide API: http://localhost:8000/api/

and the admin: http://localhost:8000/admin (admin/admin)

To process some data by hand, you can also start a python shell session into the sandbox::

    docker-compose run app python examples/sandbox/manage.py shell

To build your own audio project on top of TimeSide, just pull our latest master image::

    docker pull parisson/timeside:latest

More infos about the TimeSide docker image: https://registry.hub.docker.com/u/parisson/timeside/


Deploying
---------

Our docker composition already bundles some powerfull containers and bleeding edge frameworks like: Nginx, MySQL, RabbitMQ, Celery, Python and Django. It thus provides a safe way to deploy your project from the development stage to a massive production setup very easily.

WARNING: Before any serious production usecase, you *must* modify all the passwords and secret keys in the configuration files of the sandbox.


Scaling
--------

Thanks to Celery, each TimeSide worker of the server will process each task asynchronously over independant threads so that you can load all the cores of your CPU.

To scale it up through your cluster, Docker provides some nice tools for orchestrating it very easily: `Machine and Swarm <https://blog.docker.com/2015/02/orchestrating-docker-with-machine-swarm-and-compose/>`_.


