
Install
=======

Any platform
--------------

Thanks to Docker, TimeSide is now fully available as a docker image ready to work. The image includes all the necessary applications, modules and volumes to start your project in a few minutes.

First install `Git <http://git-scm.com/downloads>`_, `Docker <https://docs.docker.com/installation/>`_ and `docker-compose <https://docs.docker.com/compose/install/>`_, then copy these commands in a terminal and hit ENTER::

    git clone https://github.com/Parisson/TimeSide.git
    cd TimeSide
    docker-compose up

That's it! You can now browse the TimeSide API: http://localhost:8000/api/

and the admin: http://localhost:8000/admin (admin/admin)

To process some data by hand, you can also start a python shell session into the sandbox::

    docker-compose run app python examples/sandbox/manage.py shell

To build your own audido project on top of TimeSide, just pull our latest master image::

    docker pull parisson/timeside:latest

WARNING: our docker composition already bundles some powerfull containers and bleeding edge frameworks (Nginx, MySQL, RabbitMQ, Celery, Python, Django) that can be scaled from development to massive production environments very easily. But you must modify all the passwords and secret keys of the sandbox before any serious usecase.

More infos about the TimeSide docker image: https://registry.hub.docker.com/u/parisson/timeside/


Debian, Ubuntu
---------------

For Debian based distributions, we provide a safe repository giving additional dependencies that are not included in Debian yet. Please follow the instructions on `this page <http://debian.parisson.com/debian/>`_.

Some of the needed dependencies
--------------------------------

python (2.7.x) python-setuptools python-numpy python-scipy python-h5py python-matplotlib python-imaging
python-simplejson python-yaml python-mutagen libhdf5-serial-dev python-tables python-gst0.10
gstreamer0.10-gnonlin gstreamer0.10-plugins-good gstreamer0.10-plugins-bad gstreamer0.10-plugins-ugly
aubio yaafe python-aubio python-yaafe vamp-examples django (1.6.x) django-south djangorestframework django-extensions

