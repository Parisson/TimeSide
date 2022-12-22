
News
=====

1.1
---

- Core:

  - Use the libav based aubio decoder by default (fastest audio to numpy array converter on the planet!)
  - Add a VAMP based analyzer and a few plugins like VampFlatness, VampCrest, VampTempo, VampTuning, VampSpectralCentroid, VampSpectralKurtosis and VampSpectralSlope

- Server:

  - Fix a lot of asynchronous processing issues: now do every pre-processing, processing and post-processing tasks through the worker including source stream fetching from youtube
  - Add a process monitor based on websocket
  - Waveform automatically processed on Item.save()
  - Make UUID really unique
  - Reordering models
  - Improve unit tests


1.0
---

* Server refactoring:

  * audio process run on items (REST API track's model)
  * several tools, views, models and serializers
  * REST API's schema on OpenAPI 3 specification and automatic Redoc generation

* Move core and server from Python 2.7 to 3.7
* Upgrade Django to 2.2, Django REST Framework to 3.11, Celery to 4.4
* Add an `Aubio <https://github.com/aubio/aubio>`_ based decoder
* Add core and server processors' versioning and server process' run time
* Regroup all dependencies on pip requirements removing conda use
* Add :ref:`provider` as a core API component and as a REST API model
* Add provider plugins :ref:`deezer-preview`, :ref:`deezer-complete` and :ref:`youtube`
* Improve server unit testing
* Add JWT authentication on REST API
* Various bug fixes
* Add core, server and workers logging


0.9
---

* Upgrade all python dependencies
* Add Vamp, Essentia, Yaafe, librosa, PyTorch, Tensorflow libs and wrappers
* Add a few analyzing plugins (Essentia Dissonance, Vamp Constant Q, Vamp Tempo, Vamp general wrapper, Yaafe general wrapper)
* Add processor parameter management
* Add processor inheritance
* Improve HTML5 player with clever data streaming
* Improve REST API and various serialzers
* Improve unit testing
* Various bug fixes

0.8
---

* Add *Docker* support for instant installation. This allows to run TimeSide now on *any* OS platform!
* Add `Jupyter Notebook <http://jupyter.org/>`_ support for easy prototyping, experimenting and sharing (see the examples in the doc).
* Add an experimental web server and REST API based on Django REST Framework, Redis and Celery. This now provides a real web audio processing server with high scaling capabilities thanks to Docker (clustering) and Celery (multiprocessing).
* Start the development of a new player interface thanks to Angular and WavesJS.
* Huge cleanup of JS files. Please now use bower to get all JS dependencies as `listed in settings <https://github.com/Parisson/TimeSide/blob/dev/app/sandbox/settings.py#L199>`_.
* Add metadata export to Elan annotation files.
* Fix and improve some data structures in analyzer result containers.
* Many various bugfixes.

0.7.1
-----

* fix django version to 1.6.10 (sync with Telemeta 1.5)

0.7
----

* Code refactoring:

  * Create a new module `timeside.plugins` and move processors therein: timeside.plugins.decoder,analyzer, timeside.plugins.encoder, timeside.plugins.fx
  * WARNING: to properly manage the namespace packages structure, the TimeSide main module is now `timeside.core` and code should now be initialized with `import timeside.core`
  * `timeside.plugins` is now a `namespace package <https://pythonhosted.org/setuptools/setuptools.html#namespace-packages>`_ enabling external plugins to be **automatically** plugged into TimeSide (see for example `timeside-diadems <https://github.com/ANR-DIADEMS/timeside-diadems>`_). This now makes TimeSide a **real** plugin host, yeah!
  * A dummy timeside plugin will soon be provided for easy development start.

* Move all analyzers developped by the partners of the Diadems project to a new repository: `timeside-diadems <https://github.com/ANR-DIADEMS/timeside-diadems>`_
* Many fixes for a better processing by `Travis-CI <https://travis-ci.org/Parisson/TimeSide>`_
* Add a dox file to test the docker building continously on `various distributions <https://github.com/Parisson/Docker>`_

For older news, please visit: https://github.com/Parisson/TimeSide/blob/master/NEWS.rst
