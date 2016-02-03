
User Interfaces
===============

Linux
-----

Just enter a docker container with the interactive python shell::

   docker run -it parisson/timeside:latest ipython


MacOS or Windows
----------------

Same as in Linux, but you need to create a docker machine first::

   docker-machine create --driver virtualbox --virtualbox-memory 8096 timeside
   eval "$(docker-machine env timeside)"
   docker run -it parisson/timeside:latest ipython

More infos about the TimeSide docker image: https://registry.hub.docker.com/u/parisson/timeside/


Notebook
---------

You can also run your code in the wonderful `Jupyter Notebook <http://jupyter.org/>`_ which gives you a web interface to run your own code and share the results with your collaborators::

   git clone https://github.com/Parisson/TimeSide.git
   cd TimeSide
   docker-compose -f docker-compose.yml -f conf/dev.yml run --service-ports notebook
   
and then browse  http://localhost:8888 to acces the Jupyter notebook interface.

On MacOS or Windows, you will need to ask the IP of the virtual machine to docker-machine::

    docker-machine ip timeside

If it gives you for example 192.168.59.103, you should be able to browse the notebook at http://192.168.59.103:8888/

.. warning :: Running a Jupyter notebook server with this setup in a non-secured network is not safe. See `Running a notebook server <http://jupyter-notebook.readthedocs.org/en/latest/public_server.html/>`_ for a documented solution to this security problem.


Use you own data
----------------

In order to use your own data inside the container, you can mount a local directory as a volume. In this example, the local directory `foo` is mounted in `/home/foo` in the container::

   docker run -it -v foo:/home/foo parisson/timeside:latest ipython


Web Server (experimental)
-------------------------

TimeSide now includes an experimental web service with a REST API::

   git clone https://github.com/Parisson/TimeSide.git
   cd TimeSide
   docker-compose up db

This will pull all needed images for running the server and then initialize the database. Leave the session with CTRL+C and then finally do::

   docker-compose up

This will initialize everything and create a bunch a test sample boilerplate. You can browse the TimeSide API at:

    http://localhost:8000/timeside/api/

and the admin interface (login: admin, password: admin) at:

    http://localhost:8000/timeside/admin

.. note :: A documentation about using the objects and processors from the webserver will be written soon. We need help on this!

All (raw, still experimental) results are accessible at :

    http://localhost:8000/timeside/

.. tip :: On MacOS or Windows, replace "localhost" by the virtual machine IP given by `docker-machine ip timeside`

To process some data by hand in the web environment context, just start a django shell session::

   docker-compose run app manage.py shell

To run the webserver in background as a daemon, just add the `-d` option::

   docker-compose up -d


Batch
------

A shell script is provided to enable preset based and recursive processing through your command line interface::

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
