
Production
===========

Deploying
---------

Our docker composition already bundles some powerful containers and bleeding edge frameworks like: Nginx, MySQL, Redis, Celery, Django and Python. It thus provides a safe and continuous way to deploy your project from an early development stage to a massive production environment.

.. warning :: Before any serious production usecase, you *must* modify all the passwords and secret keys in the configuration files of the sandbox.

The best

Scaling
--------

Thanks to Celery, each TimeSide worker of the server will process each task asynchronously over independant threads so that you can load all the cores of your CPU.

To scale it up through your cluster, Docker provides some nice tools for orchestrating it very easily: `Machine and Swarm <https://blog.docker.com/2015/02/orchestrating-docker-with-machine-swarm-and-compose/>`_.
