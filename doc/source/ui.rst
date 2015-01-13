User Interfaces
===============

Python
-------

Of course all the TimeSide are available in our beloved python envionment.
As IPython is really great for discovering objects with completion, writing notebooks, we strongly advise to install and use it::

  sudo apt-get install ipython
  ipython
  >>> import timeside


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

Screenshot:
 .. image:: https://raw.github.com/Parisson/TimeSide/master/doc/slides/img/timeside_player_01.png

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

