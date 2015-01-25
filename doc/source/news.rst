News
=====

0.7

 * Code refactoring:

   - Create a new module `timeside.plugins` and move processors therein: timeside.plugins.decoder,analyzer, timeside.plugins.encoder, timeside.plugins.fx
   - WARNING: to properly manage the namespace packages structure, the TimeSide main module is now `timeside.core` and code should now be initialized with `import timeside.core`.
   - `timeside.plugins` is now a `namespace package <https://pythonhosted.org/setuptools/setuptools.html#namespace-packages>`_ enabling external plugins to be **automatically** plugged into TimeSide (see for example `timeside-diadems <https://github.com/ANR-DIADEMS/timeside-diadems>`_). This now makes TimeSide a **real** plugin host, yeah!
   - A dummy timeside plugin will soon be provided for easy development start.

 * Move all analyzers developped by the partners of the Diadems project to a new repository: `timeside-diadems <https://github.com/ANR-DIADEMS/timeside-diadems>`_
 * Many fixes for a better processing by `Travis-CI <https://travis-ci.org/Parisson/TimeSide>`_

0.6.1

  * Fix various minor bugs
  * Fix docker sandbox
  * Auto build docker image (https://registry.hub.docker.com/u/parisson/timeside/)

0.6

  * WARNING! some processor ids have changed. Please see the full list below.
  * NEW analyzers: IRIT Monopoly (see Processors)
  * NEW graphers: IRIT Start/Session segmentation
  * Add extensible buffering thanks to pytables (NEW dependency)
  * Add typed parameters in processors and server thanks to traits (NEW dependency)
  * Add a graph model to the pipe thanks to networkx (NEW dependency)
  * Add test sample generators based on GStreamer
  * Add a background image option for rendering analyzers
  * Add on-the-fly filtering decorators
  * Add a Docker development image and a Dockerfile
  * Add a Vagrant development box
  * Update the Debian package installation procedure
  * Results are now stored in pipe.results as as dictionnary of AnalyzerResults
  * Update various processors
  * Prevent duplication of processor in the pipe (i.e. processors sharing the same class and parameters). This also fix #60.
  * Update of Travis CI scripts https://travis-ci.org/Parisson/TimeSide/

0.5.6

  * Bugfix release
  * Fix analyzer instanciation as parent for some graphers
  * Store analyzer's results in pipe.results by uuid instead of id (fix #24)

For older news, please visit: https://github.com/Parisson/TimeSide/blob/master/NEWS.rst

