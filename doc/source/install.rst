


Install
=======

TimeSide needs some other python modules to run. The following methods explain how to install all dependencies on a Debian based system like Debian, Ubuntu, etc.. On Fedora and Red-Hat you might replace 'apt-get by 'yum', on Gentoo by 'emerge', or any other package manager you like :

.. code-block:: bash

   $ sudo apt-get update
   $ sudo apt-get install python python-pip python-setuptools python-gobject \
   python-gst0.10 gstreamer0.10-plugins-base gir1.2-gstreamer-0.10 \
   gstreamer0.10-plugins-good gstreamer0.10-plugins-bad \
   gstreamer0.10-plugins-ugly gobject-introspection python-mutagen \
   python-scipy python-h5py

   $ sudo pip install timeside

To get non-free (MP3, MP4, AAC, etc) decoding and encoding features, add Debian Multimedia repository and install the modules :

.. code-block:: bash

   $ echo "deb http://www.deb-multimedia.org stable main non-free" | sudo tee -a /etc/apt/sources.list
   $ sudo apt-get update
   $ apt-get install gstreamer0.10-lame gstreamer0.10-plugins-really-bad gstreamer0.10-plugins-ugly
