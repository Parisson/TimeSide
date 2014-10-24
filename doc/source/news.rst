News
=====

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
  * Update of Travis CI scripts https://travis-ci.org/yomguy/TimeSide/

0.5.6

  * Bugfix release
  * Fix analyzer instanciation as parent for some graphers
  * Store analyzer's results in pipe.results by uuid instead of id (fix #24)

For older news, please visit: https://github.com/yomguy/TimeSide/blob/master/NEWS.rst

