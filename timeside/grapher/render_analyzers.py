# -*- coding: utf-8 -*-
#
# Copyright (c) 2007-2014 Guillaume Pellerin <yomguy@parisson.com>
# Copyright (c) 2013-2014 Thomas Fillon <thomas@parisson.com>

# This file is part of TimeSide.

# TimeSide is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# TimeSide is distributed in the hope that it will be useful,
# but _WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with TimeSide.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division

from ..core import implements, interfacedoc, abstract, get_processor
from ..api import IGrapher
from .core import Grapher
from ..exceptions import PIDError


class DisplayAnalyzer(Grapher):

    """
    Builds a PIL image from analyzer result
    This is an Abstract base class
    """
    dpi = 72  # Web default value for Telemeta

    implements(IGrapher)
    abstract()

    @interfacedoc
    def __init__(self, width=1024, height=256, bg_color=(0, 0, 0),
                 color_scheme='default'):
        super(DisplayAnalyzer, self).__init__(width, height, bg_color,
                                              color_scheme)

        self._result_id = None
        self._id = NotImplemented
        self._name = NotImplemented

    @interfacedoc
    def process(self, frames, eod=False):
        return frames, eod

    @interfacedoc
    def post_process(self):
        parent_result = self.process_pipe.results[self._result_id]

        self.image = parent_result._render_PIL((self.image_width,
                                                self.image_height), self.dpi)

    @classmethod
    def create(cls, analyzer, result_id, grapher_id, grapher_name):

        class NewGrapher(cls):

            _id = grapher_id

            implements(IGrapher)

            @interfacedoc
            def __init__(self, width=1024, height=256, bg_color=(0, 0, 0),
                         color_scheme='default'):
                super(NewGrapher, self).__init__(width, height, bg_color,
                                                 color_scheme)

                self.parents.append(analyzer)
                # TODO : make it generic when analyzer will be "atomize"
                self._result_id = result_id

            @staticmethod
            @interfacedoc
            def id():
                return grapher_id

            @staticmethod
            @interfacedoc
            def name():
                return grapher_name

            __doc__ = """Builds a PIL image representing """ + grapher_name

        NewGrapher.__name__ = 'Display' + '.' + result_id

        return NewGrapher


# From here define new Grapher based on Analyzers
try:
    aubiopitch = get_processor('aubio_pitch')()
    DisplayAubioPitch = DisplayAnalyzer.create(analyzer=aubiopitch,
                                               result_id='aubio_pitch.pitch',
                                               grapher_id='grapher_aubio_pitch',
                                               grapher_name='Aubio Pitch')
except PIDError:
    pass

odf = get_processor('odf')()
DisplayOnsetDetectionFunction = DisplayAnalyzer.create(analyzer=odf,
                                                       result_id='odf',
                                                       grapher_id='grapher_odf',
                                                       grapher_name='Onset detection function')
wav = get_processor('waveform_analyzer')()
DisplayWaveform = DisplayAnalyzer.create(analyzer=wav,
                                         result_id='waveform_analyzer',
                                         grapher_id='grapher_waveform',
                                         grapher_name='Waveform from Analyzer')

irit4hz = get_processor('irit_speech_4hz')()
Display4hzSpeechSegmentation = DisplayAnalyzer.create(analyzer=irit4hz,
                                                      result_id='irit_speech_4hz.segments',
                                                      grapher_id='grapher_irit_speech_4hz_segments',
                                                      grapher_name='Irit 4Hz Speech Segmentation')
