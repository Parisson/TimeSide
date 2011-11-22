=======================
Howto Install TimeSide
=======================

This file describe how to install the TimeSide python package from source.


1. Install dependencies
=======================

TimeSide needs some other python modules to run.
See README for the full dependency list.

The following methods explain how to install all dependencies on a Debian based system
and espacially on Debian Squeeze 6.0 (stable). Is it now considered you have install this system correctly.

Become root. In a terminal or console, run::

    $ su

Write your root password.
Note : you can paste the full command but without the shell character '$'. 
Then::

    $ aptitude update
    $ aptitude install python python-gobject gobject-introspection python-setuptools python-xml python-mutagen \
           python-imaging python-numpy python-scipy python-gst0.10 gstreamer0.10-plugins-base gir1.0-gstreamer-0.10 \
           gstreamer0.10-fluendo-mp3 gstreamer0.10-plugins-good gstreamer0.10-plugins-bad

Add Debian multimedia repository to the apt sources.list and install Gstreamer MP3 modules::

    $ echo "deb deb http://www.debian-multimedia.org stable main" | tee -a /etc/apt/sources.list
    $ aptitude update
    $ aptitude install gstreamer0.10-fluendo-mp3 gstreamer0.10-lame


2. Install TimeSide
===================

Go into the module directory and then install::
    
    $ cd timeside
    $ python setup.py install

Or, directly from python package directory::

	$ sudo pip install timeside


3. Use TimeSide
===============

3.1. Waveform batching
----------------------

You can use waveform_batch to create some waveforms from a media (audio) directory, type::

    $ waveform_batch /path/to/media_dir /path/to/img_dir

Please use absolute paths. For example::

    $ waveform_batch /home/$user/music/mp3/ /home/$USER/images/


To change the color scheme or the size of the waveforms, edit the waveform_batch script::

    $ vi timeside/tools/waveform_batch

And change only the following variables of the GrapherScheme object::

        self.color_scheme = {
            'waveform': [ # Four (R,G,B) tuples for three main color channels for the spectral centroid method
                        (173,173,173), (147,149,196), (77,80,138), (108,66,0)
                        # this is a purple one
                        ],
            'spectrogram': [
                        (0, 0, 0), (58/4,68/4,65/4), (80/2,100/2,153/2), (90,180,100), (224,224,44), (255,60,30), (255,255,255)
                        ]}

        # Width of the image
        self.width = 2048

        # Height of the image
        self.height = 128

        # Background color
        self.bg_color = (255,255,255)

        # Force computation. By default, the class doesn't overwrite existing image files.
        self.force = False

Save the script and re-run setup::

    $ python setup.py install


3.2. Any other pipe processing !
--------------------------------

For example, a normalization and a waveform, from a python shell::

>>> import timeside

>>> decoder  =  timeside.decoder.FileDecoder('source.wav')
>>> grapher  =  timeside.grapher.Waveform()
>>> analyzer =  timeside.analyzer.MaxLevel()
>>> encoder  =  timeside.encoder.Mp3Encoder('output.mp3')
>>> (decoder | grapher | analyzer | encoder).run()
>>> grapher.render(output='image.png')
>>> print 'Level:', analyzer.result()


4. TimeSide UI
--------------

See http://code.google.com/p/timeside/wiki/UiGuide


5. More informations
====================

See the website for more examples and information about the TimeSide API:

http://code.google.com/p/timeside/

http://code.google.com/p/timeside/wiki/PythonApi

http://code.google.com/p/timeside/source/browse/trunk/timeside/api.py
