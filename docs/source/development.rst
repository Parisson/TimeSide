
Development
===========

A new plugin
------------

Thanks to the plugin architecture and the *timeside* namespace, it is possible to develop your own plugin independently and outside the core module.

An extensive example of what you can do is available in the `Dummy plugin example <https://github.com/Ircam-WAM/TimeSide-Dummy.git>`_. To link it to the core, you simply need to clone it into the ``lib/plugins/`` folder like this::

    git clone https://github.com/Ircam-WAM/TimeSide-Dummy.git lib/plugins/

Then rename the plugin, code it, etc. At the next container statup, the new plugin will be loaded automatically by the core module so that you can develop it and use it out of the box::

    docker-compose run app ipython
    >>> from timeside.core import get_processor
    >>> my_plugin = get_processor("dummy")


A new server feature
--------------------

First, setup the composition environment at the root of the project::

    echo "COMPOSE_FILE=docker-compose.yml:env/debug.yml" > .env
    docker-compose up

Then every change on the server part will be updated dynamically in the container thanks to the django debug server.

