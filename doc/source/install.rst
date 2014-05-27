Install
=======

The TimeSide engine is intended to work on all Linux and Unix like platforms.

It depends on several other python modules and compiled librairies like GStreamer. 

Debian, Ubuntu
---------------

For Debian based distributions, we provide a safe repository which provides all additional dependencies that are not included in Debian yet::

 $ echo "deb http://debian.parisson.com/debian/ stable main" | sudo tee -a /etc/apt/sources.list
 $ sudo apt-get update
 $ sudo apt-get install python-timeside

This method is known to be compatible with Debian 7 Wheezy with backports and Ubuntu 14.04 LTS. It will install additional binary packages from several audio feature extraction librairies like Aubio and Yaafe for which TimeSide has some nice processors.

Note you can also use pip if you already have already satisfied all the dependencies::

 $ sudo pip install timeside

Other Linux distributions
--------------------------

On other Linux platforms, you need to install all dependencies listed in the paragraph "Dependencies" (find all equivalent package names for your distribution). 

Then, use pip::
 
 $ sudo pip install timeside

OSX
---

The installation on OSX platforms is pretty hard at the moment because all dependencies are not in brew. But, it will be fully documented in the next release 0.5.6.

Dependencies
-------------

Needed::

 python (>=2.7) python-setuptools python-numpy python-scipy python-h5py python-matplotlib pillow 
 python-simplejson python-yaml python-mutagen libhdf5-serial-dev python-gst0.10 
 gstreamer0.10-gnonlin gstreamer0.10-plugins-good gstreamer0.10-plugins-bad gstreamer0.10-plugins-ugly 

Optional::

 aubio (>=0.4.1) yaafe python-aubio python-yaafe vamp-examples
 django (>=1.4) django-south djangorestframework django-extensions


