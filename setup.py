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

KEYWORDS = 'audio analysis features extraction transcoding graph plot HTML5 player metadata'

setup(
  name = "TimeSide",
  url='https://github.com/yomguy/TimeSide/',
  description = "open web audio processing framework",
  long_description = open('README.rst').read(),
  author = "Guillaume Pellerin, Paul Brossier, Thomas Fillon, Riccardo Zaccarelli, Olivier Guilyardi",
  author_email = "yomguy@parisson.com, piem@piem.org, thomas@parisson.com, riccardo.zaccarelli@gmail.com, olivier@samalyse.com",
  version = '0.5.1',
  install_requires = [
        'setuptools',
        'numpy',
        'mutagen',
        'pil',
        'h5py',
        'yaml',
        'simplejson',
        'scipy',
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
