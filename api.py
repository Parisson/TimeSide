# -*- coding: utf-8 -*-
#
# Copyright (c) 2009 Olivier Guilyardi <olivier@samalyse.com>
#
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

from timeside.component import Interface

class IProcessor(Interface):

    @staticmethod
    def id():
        """Return a short alphanumeric, lower-case string which uniquely
        identify this processor. Only letters and digits are allowed.
        An exception will be raised by MetaProcessor if the id is malformed or
        not unique amongst registered processors.
        
        Typically this identifier is likely to be used during HTTP requests
        and be passed as a GET parameter. Thus it should be as short as possible."""

