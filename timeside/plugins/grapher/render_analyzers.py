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

from timeside.core import implements, interfacedoc, abstract, get_processor
from timeside.core.grapher import Grapher, IGrapher
from timeside.core.exceptions import PIDError


class DisplayAnalyzer(Grapher):

    """
    image from analyzer result
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
        pipe_result = self.process_pipe.results
        analyzer_uuid = self.parents['analyzer'].uuid()
        analyzer_result = pipe_result[analyzer_uuid][self._result_id]

        fg_image = analyzer_result._render_PIL((self.image_width,
                                              self.image_height), self.dpi)
        if self._background:
            bg_uuid = self.parents['bg_analyzer'].uuid()
            bg_result = pipe_result[bg_uuid][self._bg_id]
            bg_image = bg_result._render_PIL((self.image_width,
                                              self.image_height), self.dpi)
            # convert image to grayscale
            bg_image = bg_image.convert('LA').convert('RGBA')

            # Merge background and foreground images
            from PIL.Image import blend
            fg_image = blend(fg_image, bg_image, 0.15)

        self.image = fg_image

    @classmethod
    def create(cls, analyzer, analyzer_parameters={}, result_id=None,
               grapher_id=None, grapher_name=None,
               background=None, staging=False):

        class NewGrapher(cls):

            _id = grapher_id
            _staging = staging

            implements(IGrapher)

            @interfacedoc
            def __init__(self, width=1024, height=256, bg_color=(0, 0, 0),
                         color_scheme='default'):
                super(NewGrapher, self).__init__(width, height, bg_color,
                                                 color_scheme)

                # Add a parent waveform analyzer
                if background == 'waveform':
                    self._background = True
                    bg_analyzer = get_processor('waveform_analyzer')()
                    self._bg_id = bg_analyzer.id()
                    self.parents['bg_analyzer'] = bg_analyzer
                elif background == 'spectrogram':
                    self._background = True
                    bg_analyzer = get_processor('spectrogram_analyzer')()
                    self._bg_id = bg_analyzer.id()
                    self.parents['bg_analyzer'] = bg_analyzer

                else:
                    self._background = None

                parent_analyzer = analyzer(**analyzer_parameters)
                self.parents['analyzer'] = parent_analyzer
                self._result_id = result_id

            @staticmethod
            @interfacedoc
            def id():
                return grapher_id

            @staticmethod
            @interfacedoc
            def name():
                return grapher_name

            __doc__ = """Image representing """ + grapher_name

        NewGrapher.__name__ = 'Display' + '.' + result_id

        return NewGrapher

#-------------------------------------------------
# From here define new Graphers based on Analyzers
#-------------------------------------------------

# Aubio Pitch
try:  # because of the dependencies on the Aubio librairy
    aubiopitch = get_processor('aubio_pitch')
    DisplayAubioPitch = DisplayAnalyzer.create(
        analyzer=aubiopitch,
        result_id='aubio_pitch.pitch',
        grapher_id='grapher_aubio_pitch',
        grapher_name='Pitch',
        background='spectrogram')
except PIDError:
    pass

# Onset Detection Function
odf = get_processor('onset_detection_function')
DisplayOnsetDetectionFunction = DisplayAnalyzer.create(
    analyzer=odf,
    result_id='onset_detection_function',
    grapher_id='grapher_onset_detection_function',
    grapher_name='Onset detection')

# Waveform
wav = get_processor('waveform_analyzer')
DisplayWaveform = DisplayAnalyzer.create(analyzer=wav,
                                         result_id='waveform_analyzer',
                                         grapher_id='grapher_waveform',
                                         grapher_name='Waveform from Analyzer',
                                         staging=True)

