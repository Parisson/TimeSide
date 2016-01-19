
Install and use
===============

Thanks to Docker, TimeSide is now fully available for every platform as a docker image ready to work. The image includes all the necessary applications, modules and volumes to start your project in a few seconds.

First install `Git <http://git-scm.com/downloads>`_, `Docker engine <https://docs.docker.com/installation/>`_ and `docker-compose <https://docs.docker.com/compose/install/>`_.


Linux
-----

Just enter a docker container with the interactive python shell (the timeside latest image will be automatically pulled)::

    docker run -it parisson/timeside:latest ipython


MacOS or Windows
----------------

Same as in Linux, but you need to create a docker machine first::

    docker-machine create --driver virtualbox --virtualbox-memory 8096 timeside
    eval "$(docker-machine env timeside)"
    docker run -it parisson/timeside:latest ipython

More infos about the TimeSide docker image: https://registry.hub.docker.com/u/parisson/timeside/


Advanced usage
----------------

In order to use the current working directory inside the container, mount it in a volume, for example /home/timeside::

    docker run -it -v $(pwd):/home/timeside parisson/timeside:latest ipython

You can also run your code in a `Jupyter Notebook <http://jupyter.org/>`_ ::

    git clone https://github.com/Parisson/TimeSide.git
    cd TimeSide
    docker-compose run --service-ports app sh /srv/app/deploy/notebook.sh

and then visit  http://localhost:8888 to acces the Jupyter notebook interface.

.. warning :: Security issue
Running a Jupyter notebook server with this setup in a non secure network is not safe. See `Running a notebook server<http://jupyter-notebook.readthedocs.org/en/latest/public_server.html/>`_ for a documented solution to this security problem.

On MacOS or Windows, you will need to know the IP of the virtual machine first::

    docker-machine ip timeside

If the IP is 192.168.59.103 for example, you should be able to browse the notebook system at http://192.168.59.103:8888/


Web Server (experimental)
-------------------------

TimeSide now includes an experimental web service with a REST API. You can start it up with::

    git clone https://github.com/Parisson/TimeSide.git
    cd TimeSide
    docker-compose up db

The last command is needed to initialize the database. Leave the session with CTRL+C and then finally do::

    docker-compose up

and browse the TimeSide API: http://localhost:8000/timeside/api/

or the admin: http://localhost:8000/timeside/admin (admin/admin)

all results are accessible at http://localhost:8000/timeside/

Refer to the documentation for more usage informations.

.. note :: on MacOS or Windows
replace "localhost" by the IP of the machine you got with "docker-machine ip timeside"

To process some data by hand in the web environment context, just start a django shell session::

    docker-compose run app manage.py shell

To run the webserver as a daemon::

    docker-compose up -d


Deploying
---------

Our docker composition already bundles some powerfull containers and bleeding edge frameworks like: Nginx, MySQL, Redis, Celery, Django and Python. It thus provides a safe and continuous way to deploy your project from an early development stage to a massive production environment.

.. warning :: Security issue
Before any serious production usecase, you *must* modify all the passwords and secret keys in the configuration files of the sandbox.


Scaling
--------

Thanks to Celery, each TimeSide worker of the server will process each task asynchronously over independant threads so that you can load all the cores of your CPU.

To scale it up through your cluster, Docker provides some nice tools for orchestrating it very easily: `Machine and Swarm <https://blog.docker.com/2015/02/orchestrating-docker-with-machine-swarm-and-compose/>`_.
