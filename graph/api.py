# -*- coding: utf-8 -*-
# Copyright (C) 2007 Samalyse SARL#
# Copyright (c) 2007-2009 Guillaume Pellerin <yomguy@parisson.com>

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

# Author: Guillaume Pellerin <yomguy@parisson.com>
# Author: Olivier Guilyardi <olivier@samalyse.com>

from timeside.core import *

class IMediaItemGrapher(Interface):
    """Media item visualizer driver interface"""

    def get_id():
        """Return a short id alphanumeric, lower-case string."""

    def get_name():
        """Return the graph name, such as "Waveform", "Spectral view",
        etc..
        """

    def set_colors(self, background=None, scheme=None):
        """Set the colors used for image generation. background is a RGB tuple, 
        and scheme a a predefined color theme name"""
        pass

    def render(media_item, width=None, height=None, options=None):
        """Generator that streams the graph output as a PNG image"""
