#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup
import sys
from setuptools.command.test import test as TestCommand


# Pytest
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['tests', '--ignore', 'tests/sandbox', '--verbose']
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


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

KEYWORDS = 'audio analysis features extraction MIR transcoding graph visualize plot HTML5 interactive metadata player'

setup(
    name='TimeSide',
    url='https://github.com/yomguy/TimeSide/',
    description="open web audio processing framework",
    long_description=open('README.rst').read(),
    author="Guillaume Pellerin, Paul Brossier, Thomas Fillon, Riccardo Zaccarelli, Olivier Guilyardi",
    author_email="yomguy@parisson.com, piem@piem.org, thomas@parisson.com, riccardo.zaccarelli@gmail.com, olivier@samalyse.com",
    version='0.6.2',
    install_requires=[
        'numpy',
        'mutagen',
        'pillow',
        'h5py',
        'tables',
        'pyyaml',
        'simplejson',
        'scipy',
        'matplotlib',
        'django==1.6.8',
        'django-extensions',
        'djangorestframework',
        'south',
        'traits',
        'networkx',
        ],
    platforms=['OS Independent'],
    license='Gnu Public License V2',
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    packages=['timeside'],
    include_package_data=True,
    zip_safe=False,
    scripts=['scripts/timeside-waveforms', 'scripts/timeside-launch'],
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    )
