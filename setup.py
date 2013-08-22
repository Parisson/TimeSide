#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

CLASSIFIERS = [
    'Intended Audience :: Science/Research',
    'Intended Audience :: Developers',
    'Intended Audience :: Information Technology',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Multimedia :: Sound/Audio',
    'Topic :: Multimedia :: Sound/Audio :: Analysis',
    'Topic :: Multimedia :: Sound/Audio :: Players',
    'Topic :: Multimedia :: Sound/Audio :: Conversion',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: Software Development :: Libraries :: Python Modules',
    ]

KEYWORDS = 'audio analyze transcode graph player metadata'

setup(
  name = "TimeSide",
  url='http://code.google.com/p/timeside',
  description = "open and fast web audio components",
  long_description = open('README.rst').read(),
  author = "Guillaume Pellerin, Paul Brossier, Riccardo Zaccarelli, Olivier Guilyardi",
  author_email = "yomguy@parisson.com, piem@piem.org, riccardo.zaccarelli@gmail.com, olivier@samalyse.com",
  version = '0.4.5',
  install_requires = [
        'setuptools',
        'numpy',
        'mutagen',
        'pil',
        ],
  platforms=['OS Independent'],
  license='Gnu Public License V2',
  classifiers = CLASSIFIERS,
  keywords = KEYWORDS,
  packages = find_packages(),
  include_package_data = True,
  zip_safe = False,
  scripts=['scripts/timeside-waveforms'],
)
