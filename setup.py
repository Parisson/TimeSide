#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

# Utility function to read file in the setup.py directory


def open_here(fname):
    return open(os.path.join(os.path.dirname(__file__), fname))


def get_dependencies(env_yml_file):
    """
    Read the dependencies from a Conda environment file in YAML
    and return a list of such dependencies (from conda and pip list)
    Be sure to match packages specification for each of:
    - Conda : http://conda.pydata.org/docs/spec.html#build-version-spec
    - Pip & Setuptool :
       - http://pythonhosted.org/setuptools/setuptools.html?highlight=install_require#declaring-dependencies
       - https://pythonhosted.org/setuptools/pkg_resources.html#requirement-objects
    """
    import yaml
    with open_here(env_yml_file) as f:
        environment = yaml.load(f)
    conda_dependencies = []
    package_map = {
        'pytables': 'tables',  # insert 'tables' instead of 'pytables'
        'yaafe': '',
        'essentia': '',
        'pytorch': '',
        # Yaafe and essentia are not seen by pip during pip install -e .
        # and not visible with pip list
        # TODO: check if setuptools can help
    }
    for dep in environment['dependencies']:
        if isinstance(dep, str) and not(dep.startswith('python')):
            if dep in package_map:
                conda_dependencies.append(package_map[dep])
            else:
                conda_dependencies.append(dep)
        elif isinstance(dep, dict) and 'pip' in dep:
            pip_dependencies = dep['pip']

    return pip_dependencies

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
    url='https://github.com/Parisson/TimeSide/',
    description="Audio processing framework for the web",
    long_description=open_here('README.rst').read(),
    author="Guillaume Pellerin, Paul Brossier, Thomas Fillon, Riccardo Zaccarelli, Olivier Guilyardi",
    author_email="yomguy@parisson.com, piem@piem.org, thomas@parisson.com, riccardo.zaccarelli@gmail.com, olivier@samalyse.com",
    version='0.9.6',
    setup_requires=['pyyaml'],
    install_requires=[get_dependencies('environment-pinned.yml')],
    platforms=['OS Independent'],
    license='Gnu Public License V2',
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    packages=['timeside'],
    include_package_data=True,
    zip_safe=False,
    scripts=['bin/timeside-waveforms', 'bin/timeside-launch'],
    tests_require=['pytest>=3', 'pytest-django'],
    cmdclass={'test': PyTest},
)
