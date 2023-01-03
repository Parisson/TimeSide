
Production
===========

First, setup the composition environment at the root of the project::

    echo "COMPOSE_FILE=docker-compose.yml:env/prod.yml" > .env

Deploying
---------

The docker composition already bundles some powerful containers based on: Nginx, PostgreSQL, Redis, Celery, Django, Django REST Framework, Python and various related librairies. It thus provides a safe and continuous way to deploy your project from an early development stage to a massive production environment.

.. warning :: Before any serious production usecase, you *must* modify all the passwords and secret keys in the configuration files of the sandbox.

Scaling
--------

The Celery based worker container scales on all local CPUs automatically so that each processing pipelines is run asynchronously from its own thread. To scale on more machines, Kubernetes should offer evrything like demonstrated in these tutorials:

  - https://learnk8s.io/scaling-celery-rabbitmq-kubernetes
  - https://blog.devgenius.io/django-celery-in-kubernetes-for-scheduling-tasks-12718ef38bce

A Google Cloud based configuration is provided as an example in the k8s/ directory.

