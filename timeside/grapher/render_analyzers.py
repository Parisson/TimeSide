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
        parent_uuid = self.parents['analyzer'].uuid()
        parent_result = pipe_result[parent_uuid][self._result_id]

        fg_image = parent_result._render_PIL((self.image_width,
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
            fg_image = blend(fg_image, bg_image, 0.25)

        self.image = fg_image

    @classmethod
    def create(cls, analyzer, analyzer_parameters={}, result_id=None,
               grapher_id=None, grapher_name=None,
               background=None):

        class NewGrapher(cls):

            _id = grapher_id

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
                # TODO : make it generic when analyzer will be "atomize"
                self._parent_uuid =  parent_analyzer.uuid()
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
                                         grapher_name='Waveform from Analyzer')

# IRIT 4Hz
irit4hz = get_processor('irit_speech_4hz')
Display4hzSpeechSegmentation = DisplayAnalyzer.create(
    analyzer=irit4hz,
    result_id='irit_speech_4hz.segments',
    grapher_id='grapher_irit_speech_4hz_segments',
    grapher_name='Speech segmentation',
    background='waveform')


# IRIT 4Hz with median filter
irit4hz = get_processor('irit_speech_4hz')
Display4hzSpeechSegmentation = DisplayAnalyzer.create(
    analyzer=irit4hz,
    result_id='irit_speech_4hz.segments_median',
    grapher_id='grapher_irit_speech_4hz_segments_median',
    grapher_name='Speech segmentation (median)',
    background='waveform')

# IRIT Monopoly
try:  # because of the dependencies on Aubio Pitch
    iritmonopoly = get_processor('irit_monopoly')
    DisplayMonopoly = DisplayAnalyzer.create(
        analyzer=iritmonopoly,
        result_id='irit_monopoly.segments',
        grapher_id='grapher_monopoly_segments',
        grapher_name='Mono/Poly segmentation',
        background='waveform')
except PIDError:
    pass

# Limsi SAD : 2 models
try:
    limsi_sad = get_processor('limsi_sad')

    DisplayLIMSI_SAD_etape = DisplayAnalyzer.create(
        analyzer=limsi_sad,
        analyzer_parameters={'sad_model': 'etape'},
        result_id='limsi_sad.sad_lhh_diff',
        grapher_id='grapher_limsi_sad_etape',
        grapher_name='Speech activity (ETAPE)',
        background='waveform')

    DisplayLIMSI_SAD_maya = DisplayAnalyzer.create(
        analyzer=limsi_sad,
        analyzer_parameters={'sad_model': 'maya'},
        result_id='limsi_sad.sad_lhh_diff',
        grapher_id='grapher_limsi_sad_maya',
        grapher_name='Speech activity (Mayan)',
        background='waveform')

except PIDError:
    pass

# IRIT Start Seg
irit_startseg = get_processor('irit_startseg')
DisplayIRIT_Start = DisplayAnalyzer.create(
    analyzer=irit_startseg,
    result_id='irit_startseg.segments',
    grapher_id='grapher_irit_startseg',
    grapher_name='Analogous start point',
    background='waveform')
