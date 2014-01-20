# -*- coding: utf-8 -*-
#
# Copyright (c) 2007-2014 Guillaume Pellerin <yomguy@parisson.com>
# Copyright (c) 2010 Olivier Guilyardi <olivier@samalyse.com>
# Copyright (c) 2013-2014 Thomas Fillon <thomas@parisson.com>

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
from __future__ import division

from timeside.core import implements, interfacedoc
from timeside.api import IGrapher
from timeside.grapher.core import *


class DisplayAnalyzers(Grapher):
    """ Builds a PIL image ..."""
    dpi = 72  # Web default value for Telemeta

    implements(IGrapher)
    abstract()

    @interfacedoc
    def __init__(self, width=1024, height=256, bg_color=(0, 0, 0),
                 color_scheme='default'):
        super(DisplayAnalyzers, self).__init__(width, height, bg_color,
                                               color_scheme)
        self.dpi = 72

    @interfacedoc
    def process(self, frames, eod=False):
        return frames, eod

    @interfacedoc
    def post_process(self):
        parent_result = self.process_pipe.results[self.analyzer_id]

        fig = parent_result.render((self.image_width,
                                    self.image_height), self.dpi)

        # Export to PIL image
        import StringIO
        imgdata = StringIO.StringIO()
        fig.savefig(imgdata, format='png', dpi=self.dpi)
        imgdata.seek(0)  # rewind the data
        self.image = Image.open(imgdata)


class DisplayAubioPitch(DisplayAnalyzers):

    implements(IGrapher)

    @interfacedoc
    def __init__(self, width=1024, height=256, bg_color=(0, 0, 0),
                 color_scheme='default'):
        super(DisplayAubioPitch, self).__init__(width, height, bg_color,
                                                color_scheme)

        # Analyzer definition  --> change this to implement a new analyzer
        from timeside.analyzer import AubioPitch
        self.parents.append(AubioPitch())
        self.analyzer_id = 'aubio_pitch.pitch'  # TODO : make it generic when analyzer will be "atomize"

    @staticmethod
    @interfacedoc
    def id():
        return "grapher_aubio_pitch"

    @staticmethod
    @interfacedoc
    def name():
        return "Grapher for Aubio Pitch"
