Install
=======


TimeSide needs some other python modules to run. The following methods explain how to install all dependencies on various Linux based systems.

On Debian, Ubuntu, etc:

.. code-block:: bash

 $ echo "deb http://debian.parisson.com/debian/ stable main" | sudo tee -a /etc/apt/sources.list
 $ sudo apt-get update
 $ sudo apt-get install python-timeside

On other system, you'll need to install the Gstreamer framework and modules, aubio (>=0.4), yaafe (>=0.64) and some more programs.
For example on Fedora and Red-Hat:

.. code-block:: bash

 $ sudo yum install gcc python python-devel gstreamer pygobject2 gstreamer-python  \
                   gstreamer gstreamer-plugins-bad-free gstreamer-plugins-bad-free-extras \
                   gstreamer-plugins-base gstreamer-plugins-good

 $ sudo pip install timeside

