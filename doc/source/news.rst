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
