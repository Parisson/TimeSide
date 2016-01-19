==================================================
TimeSide : audio processing framework for the web
==================================================

|version| |downloads| |travis_master| |coveralls_master|

.. |travis_master| image:: https://secure.travis-ci.org/Parisson/TimeSide.png?branch=master
    :target: https://travis-ci.org/Parisson/TimeSide/

.. |coveralls_master| image:: https://coveralls.io/repos/Parisson/TimeSide/badge.png?branch=master
  :target: https://coveralls.io/r/Parisson/TimeSide?branch=master

.. |version| image:: https://img.shields.io/pypi/v/timeside.svg
   :target: https://pypi.python.org/pypi/TimeSide/
   :alt: Version

.. |downloads| image:: https://img.shields.io/pypi/dm/timeside.svg
   :target: https://pypi.python.org/pypi/TimeSide/
   :alt: Downloads


TimeSide is a python framework enabling low and high level audio analysis, imaging, transcoding, streaming and labelling. Its high-level API is designed to enable complex processing on very large datasets of any audio or video assets with a plug-in architecture, a secure scalable backend and an extensible dynamic web frontend.


Use cases
==========

* Scaled audio computing (filtering, machine learning, etc)
* Web audio visualization
* Plugin prototyping
* Pseudo-realtime transcoding and streaming
* Automatic segmentation and labelling synchronized with audio events


Goals
=====

* **Do** asynchronous and fast audio processing with Python,
* **Decode** audio frames from **any** audio or video media format into numpy arrays,
* **Analyze** audio content with some state-of-the-art audio feature extraction libraries like Aubio, Yaafe and VAMP as well as some pure python processors
* **Visualize** sounds with various fancy waveforms, spectrograms and other cool graphers,
* **Transcode** audio data in various media formats and stream them through web apps,
* **Serialize** feature analysis data through various portable formats,
* **Playback** and **interact** **on demand** through a smart high-level HTML5 extensible player,
* **Index**, **tag** and **annotate** audio archives with semantic metadata (see `Telemeta <http://telemeta.org>`__ which embed TimeSide).
* **Deploy** and **scale** your own audio processing engine through any infrastructure


Funding and support
===================

To fund the project and continue our fast development process, we need your explicit support. So if you use TimeSide in production or even in development, please let us know:

* star or fork the project on `GitHub <https://github.com/Parisson/TimeSide>`_
* tweet something to `@parisson_studio <https://twitter.com/parisson_studio>`_ or `@yomguy <https://twitter.com/omguy>`_
* drop us an email <support@parisson.com>

Thanks for your help!

Architecture
============

The streaming architecture of TimeSide relies on 2 main parts: a processing engine including various plugin processors written in pure Python and a user interface providing some web based visualization and playback tools in pure HTML5.

.. image:: http://vcs.parisson.com/gitweb/?p=timeside.git;a=blob_plain;f=doc/images/TimeSide_pipe.svg;hb=refs/heads/dev
  :width: 800 px

Dive in
========

Let's produce a really simple audio analysis of an audio file.
First, list all available plugins:


>>> import timeside.core
>>> timeside.core.list_processors()

Define some processors:


>>> from timeside.core import get_processor
>>> from timeside.core.tools.test_samples import samples
>>> wavfile = samples['sweep.wav']
>>> decoder  =  get_processor('file_decoder')(wavfile)
>>> grapher  =  get_processor('waveform_simple')()
>>> analyzer =  get_processor('level')()
>>> encoder  =  get_processor('vorbis_encoder')('sweep.ogg')

Then run the *magic* pipeline:


>>> (decoder | grapher | analyzer | encoder).run()

Render the grapher results:


>>> grapher.render(output='waveform.png')

Show the analyzer results:


    Level: {'level.max': AnalyzerResult(...)}


So, in only one pass, the audio file has been decoded, analyzed, graphed and transcoded.

For more extensive examples, please see the `full documentation <http://files.parisson.com/timeside/doc/>`_.
News
=====

0.8

* Add *Docker* support for instant installation across any OS platform (see Install and use)
* Add `Jupyter Notebook <http://jupyter.org/>`_ support for easy experimental writing and sharing
* Add an experimental web server and REST API based on Django REST Framework, Celery, Angular and WavesJS.
* Add metadata export to Elan annotation files.
* Fix and improve some data structures in analyzer result containers
* Various bugfixes
* See Release notes

0.7.1

* fix django version to 1.6.10 (sync with Telemeta 1.5)

0.7

* Code refactoring:

   - Create a new module `timeside.plugins` and move processors therein: timeside.plugins.decoder,analyzer, timeside.plugins.encoder, timeside.plugins.fx
   - WARNING: to properly manage the namespace packages structure, the TimeSide main module is now `timeside.core` and code should now be initialized with `import timeside.core`
   - `timeside.plugins` is now a `namespace package <https://pythonhosted.org/setuptools/setuptools.html#namespace-packages>`_ enabling external plugins to be **automatically** plugged into TimeSide (see for example `timeside-diadems <https://github.com/ANR-DIADEMS/timeside-diadems>`_). This now makes TimeSide a **real** plugin host, yeah!
   - A dummy timeside plugin will soon be provided for easy development start.

* Move all analyzers developped by the partners of the Diadems project to a new repository: `timeside-diadems <https://github.com/ANR-DIADEMS/timeside-diadems>`_
* Many fixes for a better processing by `Travis-CI <https://travis-ci.org/Parisson/TimeSide>`_
* Add a dox file to test the docker building continously on `various distributions <https://github.com/Parisson/Docker>`_

For older news, please visit: https://github.com/Parisson/TimeSide/blob/master/NEWS.rst
API / Documentation
====================

* General : http://files.parisson.com/timeside/doc/
* Tutorial : http://files.parisson.com/timeside/doc/tutorial/index.html
* API : http://files.parisson.com/timeside/doc/api/index.html
* Publications : https://github.com/Parisson/Telemeta-doc
* Player / UI : https://github.com/Parisson/TimeSide/wiki/Ui-Guide (see also "Web player")
* Notebooks : http://nbviewer.ipython.org/github/thomasfillon/Timeside-demos/tree/master/
* Example : http://archives.crem-cnrs.fr/archives/items/CNRSMH_E_2004_017_001_01/

Install and start
=================

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


Webserver (experimental)
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
User Interfaces
===============

Python
-------

Of course all the TimeSide are available in our beloved python envionment.
As IPython is really great for discovering objects with completion, writing notebooks, we strongly advise to install and use it::

  sudo apt-get install ipython
  ipython
  >>> import timeside.core


Shell
------

Of course, TimeSide can be used in any python environment. But, a shell script is also provided to enable preset based and recursive processing through your command line interface::

 timeside-launch -h
 Usage: scripts/timeside-launch [options] -c file.conf file1.wav [file2.wav ...]
  help: scripts/timeside-launch -h

 Options:
  -h, --help            show this help message and exit
  -v, --verbose         be verbose
  -q, --quiet           be quiet
  -C <config_file>, --conf=<config_file>
                        configuration file
  -s <samplerate>, --samplerate=<samplerate>
                        samplerate at which to run the pipeline
  -c <channels>, --channels=<channels>
                        number of channels to run the pipeline with
  -b <blocksize>, --blocksize=<blocksize>
                        blocksize at which to run the pipeline
  -a <analyzers>, --analyzers=<analyzers>
                        analyzers in the pipeline
  -g <graphers>, --graphers=<graphers>
                        graphers in the pipeline
  -e <encoders>, --encoders=<encoders>
                        encoders in the pipeline
  -R <formats>, --results-formats=<formats>
                        list of results output formats for the analyzers
                        results
  -I <formats>, --images-formats=<formats>
                        list of graph output formats for the analyzers results
  -o <outputdir>, --ouput-directory=<outputdir>
                        output directory


Find some preset examples in examples/presets/


Web player
-----------

TimeSide comes with a smart and pure **HTML5** audio player.

Features:

* embed it in any audio web application
* stream, playback and download various audio formats on the fly
* synchronize sound with text, bitmap and vectorial events
* seek through various semantic, analytic and time synced data
* fully skinnable with CSS style

.. image:: https://raw.githubusercontent.com/Parisson/TimeSide/dev/doc/images/timeside_player_01.png
  :alt: TimeSide player

Examples of the player embeded in the Telemeta open web audio CMS:

* http://parisson.telemeta.org/archives/items/PRS_07_01_03/
* http://archives.crem-cnrs.fr/items/CNRSMH_I_1956_002_001_01/

Development documentation:

* https://github.com/Parisson/TimeSide/wiki/Ui-Guide

TODO list:

* zoom
* layers


Web server
-----------

An EXPERIMENTAL web server based on Django has been added to the package from version 0.5.5. The goal is to provide a full REST API to TimeSide to enable new kinds of audio processing web services.

A sandbox is provided in timeside/server/sandbox and you can initialize it and test it like this::

  cd examples/sandbox
  ./manage.py syncdb
  ./manage.py migrate
  ./manage.py runserver

and browse http://localhost:8000/api/

At the moment, this server is NOT connected to the player using TimeSide alone. Please use Telemeta.
Development
===========

|travis_dev| |coveralls_dev|

.. |travis_dev| image:: https://secure.travis-ci.org/Parisson/TimeSide.png?branch=dev
    :target: https://travis-ci.org/Parisson/TimeSide/

.. |coveralls_dev| image:: https://coveralls.io/repos/Parisson/TimeSide/badge.png?branch=dev
  :target: https://coveralls.io/r/Parisson/TimeSide?branch=dev

The easiest way to develop with TimeSide framework is to use our `DevBox <https://github.com/Parisson/DevBox>`_

First, install Docker: https://docs.docker.com/installation/

Then, simply pull the image and run it::

  docker pull parisson/timeside
  docker run -p 9000:80 parisson/timeside

You can now browse the TimeSide API: http://localhost:9000/api/

or get a shell session::

  docker run -ti parisson/timeside bash

To start a new development, it is advised to checkout the dev branch in the container::

  cd /opt/TimeSide
  git checkout dev

or get our latest-dev image::

  docker pull parisson/timeside:latest-dev

More infos: https://registry.hub.docker.com/u/parisson/timeside/
Sponsors and Partners
=====================

* `Parisson <http://parisson.com>`_
* `CNRS <http://www.cnrs.fr>`_ (National Center of Science Research, France)
* `Huma-Num <http://www.huma-num.fr/>`_ (big data equipment for digital humanities, ex TGE Adonis)
* `CREM <http://www.crem-cnrs.fr>`_ (french National Center of Ethomusicology Research, France)
* `Université Pierre et Marie Curie <http://www.upmc.fr>`_ (UPMC Paris, France)
* `ANR <http://www.agence-nationale-recherche.fr/>`_ (CONTINT 2012 project : DIADEMS)
* `MNHN <http://www.mnhn.fr>`_ : Museum National d'Histoire Naturelle (Paris, France)


Related projects
=================

* `Telemeta <http://telemeta.org>`__ : open web audio platform
* `Sound archives <http://archives.crem-cnrs.fr/>`_ of the CNRS, CREM and the "Musée de l'Homme" in Paris, France.
* The `DIADEMS project <http://www.irit.fr/recherches/SAMOVA/DIADEMS/en/welcome/>`_ sponsored by the ANR.

Copyrights
==========

* Copyright (c) 2006, 2016 Parisson Sarl
* Copyright (c) 2006, 2016 Guillaume Pellerin
* Copyright (c) 2013, 2016 Thomas Fillon
* Copyright (c) 2010, 2014 Paul Brossier
* Copyright (c) 2013, 2014 Maxime Lecoz
* Copyright (c) 2013, 2014 David Doukhan
* Copyright (c) 2006, 2010 Olivier Guilyardi


License
=======

TimeSide is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

TimeSide is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

See LICENSE for more details.
