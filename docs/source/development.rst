
Development
===========

First, setup the composition environment at the root of the project::

    echo "COMPOSE_FILE=docker-compose.yml:env/debug.yml" > .env


Developing the framework
------------------------

Thanks to the docker composition, the timeside module is dynamically loaded into the app container. So you can develop the module from the host and use it into the container. For example::

     docker-compose run app ipython
     >>> import timeside

It is exactly the same idea for the server part which you can update dynamically thanks to the django debug server after starting up::

    docker-compose up -d


Developing your own external plugins
------------------------------------

If the (already huge) python module bundle provided by TimeSide is to short for you, it is possible to make your own plugin bundle outside the core module thanks to the TimeSide namespace. An extensive example of what you can do is available in the `DIADEMS project repository <https://github.com/ANR-DIADEMS/timeside-diadems/>`_. You can also start with the dummy plugin::

    git clone https://github.com/Parisson/TimeSide-Dummy.git lib/plugins/

Rename it, code it, etc. At the next statup, the new plugins will be loaded automatically. For example, you could do::

    docker-compose run app ipython
    >>> import timeside

or, for the server::

    docker-compose restart app


