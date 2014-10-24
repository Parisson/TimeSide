Install
=======

The TimeSide engine is intended to work on all Linux and Unix like platforms. It depends on several other python modules and compiled libraries like GStreamer.

Debian, Ubuntu
---------------

For Debian based distributions, we provide a safe repository giving additional dependencies that are not included in Debian yet. Please follow the instructions on `this page <http://debian.parisson.com/debian/>`_.

Other Linux distributions
--------------------------

On other Linux platforms, you need to install all dependencies listed in Dependencies finding all equivalent package names for your distribution.

Then, use pip::

 sudo pip install timeside

OSX / Windows
--------------

Native install is hard at the moment but you can either run our Vagrant or Docker images (see Development).

Dependencies
-------------

Needed:

 python (>=2.7) python-setuptools python-numpy python-scipy python-h5py python-matplotlib python-imaging
 python-simplejson python-yaml python-mutagen libhdf5-serial-dev python-tables python-gst0.10
 gstreamer0.10-gnonlin gstreamer0.10-plugins-good gstreamer0.10-plugins-bad gstreamer0.10-plugins-ugly

Optional:

 aubio (>=0.4.1) yaafe python-aubio python-yaafe vamp-examples
 django (>=1.4) django-south djangorestframework django-extensions

