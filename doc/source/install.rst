Install
=======

TimeSide needs some other python modules to run. The following methods explain how to install all dependencies on various Linux based systems.

On Debian, Ubuntu, etc:

.. code-block:: bash

 $ echo "deb http://debian.parisson.com/debian/ stable main" | sudo tee -a /etc/apt/sources.list
 $ sudo apt-get update
 $ sudo apt-get install python-timeside

On Fedora and Red-Hat:

.. code-block:: bash

 $ sudo yum install gcc python python-devel gstreamer pygobject2 \
                   gstreamer-python gstreamer gstreamer-plugins-bad-free \
                   gstreamer-plugins-bad-free-extras \
                   gstreamer-plugins-base gstreamer-plugins-good

 $ sudo pip install timeside

On other system, you'll need to install all dependencies and then::

 $ sudo pip install timeside


Dependencies
============

python (>=2.7), python-setuptools, python-gst0.10, gstreamer0.10-plugins-good, gstreamer0.10-gnonlin,
gstreamer0.10-plugins-ugly, python-aubio, python-yaafe, python-simplejson, python-yaml, python-h5py,
python-scipy


Platforms
==========

The TimeSide engine is intended to work on all Unix / Linux platforms.
MacOS X and Windows versions will soon be explorated.
The player should work on any modern HTML5 enabled browser.
Flash is needed for MP3 if the browser doesn't support it.

