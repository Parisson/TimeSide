#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2007-2013 Parisson SARL

# This file is part of TimeSide.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Authors:
#   Thomas Fillon <thomas  at parisson.com>
import unittest
from unit_timeside import TestRunner
import doctest
import timeside
from timeside.core.tools.package import discover_modules


def load_tests(loader, tests, ignore):

    finder = doctest.DocTestFinder(exclude_empty=False)

    # Create tests for doctest in timeside modules and sub-modules
    modules_list = discover_modules(timeside.__name__)

    for module in modules_list:
        _tmp = __import__(module, fromlist=['DOCTEST_ALIAS'])
        try:
            DOCTEST_ALIAS = _tmp.DOCTEST_ALIAS
        except AttributeError:
            DOCTEST_ALIAS = {}

        tests.addTests(doctest.DocTestSuite(module, extraglobs=DOCTEST_ALIAS,
                                            test_finder=finder))

    return tests


if __name__ == '__main__':
    import os
     # Do not run doctest for environment without a display (e.g. server)
    if 'DISPLAY' in os.environ:
        unittest.main(testRunner=TestRunner())
