# -*- coding: utf-8 -*-
#
# Copyright (c) 2007-2013 Parisson SARL

# This file is part of TimeSide.

# TimeSide is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# TimeSide is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with TimeSide.  If not, see <http://www.gnu.org/licenses/>.

# Authors:
#   Thomas Fillon <thomas  at parisson.com>


import unittest
import doctest
import timeside
import pkgutil


def load_tests(loader, tests, ignore):

    import fnmatch
    import os

    finder = doctest.DocTestFinder(exclude_empty=False)

    timeside_path = os.path.dirname(timeside.__path__[0])

    # Create tests for doctest ReST files
    rst_files = []
    for root, dirnames, filenames in os.walk(timeside_path):
        for filename in fnmatch.filter(filenames, '*.rst'):
            rst_files.append(os.path.join(root, filename))

    for filename in rst_files:
        tests.addTests(doctest.DocFileSuite(filename, module_relative=False))

    # Create tests for doctest in timeside modules and sub-modules
    modules_list = [modname for _, modname, _ in pkgutil.walk_packages(
                    path=timeside.__path__,
                    prefix=timeside.__name__ + '.',
                    onerror=lambda x: None)]

    for module in modules_list:
        tests.addTests(doctest.DocTestSuite(module, test_finder=finder))

    return tests


if __name__ == '__main__':
    unittest.main()
