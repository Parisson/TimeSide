Install
=======

The TimeSide engine is intended to work on all Linux and Unix like platforms.

It depends on several other python modules and compiled librairies like GStreamer.

Debian, Ubuntu
---------------

For Debian based distributions, we provide a safe repository which provides all additional dependencies that are not included in Debian yet. Please follow the instructions on `this page <http://debian.parisson.com/debian/>`_.

Other Linux distributions
--------------------------

On other Linux platforms, you need to install all dependencies listed in the paragraph "Dependencies" (find all equivalent package names for your distribution).

Then, use pip::

 sudo pip install timeside

OSX
---

The installation on OSX platforms is pretty hard at the moment because all dependencies are not in brew. But, it will be fully documented in the next release 0.5.6.

Dependencies
-------------

Needed:

 python (>=2.7) python-setuptools python-numpy python-scipy python-h5py python-matplotlib python-imaging
 python-simplejson python-yaml python-mutagen libhdf5-serial-dev python-tables python-gst0.10
 gstreamer0.10-gnonlin gstreamer0.10-plugins-good gstreamer0.10-plugins-bad gstreamer0.10-plugins-ugly

Optional:

 aubio (>=0.4.1) yaafe python-aubio python-yaafe vamp-examples
 django (>=1.4) django-south djangorestframework django-extensions

