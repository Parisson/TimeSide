#!/usr/bin/env python

'''The setup and build script for the python-twitter library.'''

__author__ = 'yomguy@parisson.com'
__version__ = '0.1-beta'


# The base package metadata to be used by both distutils and setuptools
METADATA = dict(
  name = "timeside",
  version = __version__,
  py_modules = ['timeside'],
  description='Web Audio Components',
  author='Olivier Guilyardi, Paul Brossier, Guillaume Pellerin',
  author_email='yomguy@parisson.com',
  license='Gnu Public License V2',
  url='http://code.google.com/p/timeside',
  packages=['timeside'],
  keywords='audio analyze transcode graph',
  install_requires = ['setuptools',]
  include_package_data = True,
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
