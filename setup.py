#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


# Utility function to read file in the setup.py directory
def open_here(fname):
    return open(os.path.join(os.path.dirname(__file__), fname))


# Pytest
class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['tests', '--ignore', 'tests/sandbox', '--verbose', '--ds=app.test_settings']
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
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
    url='https://github.com/Ircam-WAM/TimeSide/',
    description="Audio processing framework for the web",
    long_description=open_here('README.rst').read(),
    author="Guillaume Pellerin, Paul Brossier, Thomas Fillon, Riccardo Zaccarelli, Olivier Guilyardi",
    author_email="yomguy@parisson.com, piem@piem.org, thomas@parisson.com, riccardo.zaccarelli@gmail.com, olivier@samalyse.com",
    version='1.1.1',
    platforms=['OS Independent'],
    license='Affero Gnu Public License v2',
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    tests_require=['pytest>=3', 'pytest-django'],
    cmdclass={'test': PyTest},
)
