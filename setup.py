#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''The setup and build script for the python-twitter library.'''

__author__ = 'yomguy@parisson.com'
__version__ = '0.3'


# The base package metadata to be used by both distutils and setuptools
METADATA = dict(
  name = "TimeSide",
  version = __version__,
  py_modules = ['timeside'],
  description='Web Audio Components',
  author='Olivier Guilyardi, Paul Brossier, Guillaume Pellerin, Riccardo Zaccarelli',
  author_email='yomguy@parisson.com',
  license='Gnu Public License V2',
  url='http://code.google.com/p/timeside',
  packages=['timeside','timeside.decoder','timeside.encoder','timeside.grapher',
            'timeside.analyzer','timeside.tests','timeside.tests.api'],
  keywords='audio analyze transcode graph player metadata',
  install_requires = ['setuptools',],
  include_package_data = True,
  classifiers = ['Intended Audience :: Science/Research', 'Programming Language :: Python', 'Programming Language :: JavaScript', 'Topic :: Internet :: WWW/HTTP :: Dynamic Content', 'Topic :: Multimedia :: Sound/Audio', 'Topic :: Multimedia :: Sound/Audio :: Analysis', 'Topic :: Multimedia :: Sound/Audio :: Players', 'Topic :: Scientific/Engineering :: Information Analysis', ],
  
)


def Main():
  # Use setuptools if available, otherwise fallback and use distutils
  try:
    import setuptools
    setuptools.setup(**METADATA)
  except ImportError:
    import distutils.core
    distutils.core.setup(**METADATA)


if __name__ == '__main__':
  Main()
