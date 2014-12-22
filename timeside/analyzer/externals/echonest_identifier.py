# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Guillaume Pellerin <yomguy@parisson.com>

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

# Author: Thomas Fillon <thomas@parisson.com>

from timeside.core import implements, interfacedoc
from timeside.analyzer.core import Analyzer
from timeside.api import IAnalyzer
from timeside.analyzer.preprocessors import downmix_to_mono
import numpy as np
import echoprint
import requests
import struct
import os
import json
from threading import Thread


class EchoNestIdentifier(Analyzer):
    """EchoNest identifier based on libcodegen and echoprint

    Example:

        file_decoder = get_processor('file_decoder')
        echo_analyzer = get_processor('echonest_identifier')
        decoder = file_decoder(uri=uri, start=0, duration=20)
        analyzer = echo_analyzer(start=0)
        decoder.output_samplerate = 11025
        pipe = (decoder | analyzer)
        pipe.run()
        songs = analyzer.metadata['songs']
        if songs:
            print songs[0]['artist_name'] + ' - ' + songs[0]['title']
        else:
            print 'Unknown'

    """

    implements(IAnalyzer)

    needs = ['https://github.com/yomguy/python-echoprint',]
    api_url = 'http://developer.echonest.com/api/v4/song/identify'
    api_key = '6O3QX1BEQVY0JDDU5'
    proxy = None
    delay = 1

    def __init__(self, api_key=None, start=-1):
        super(EchoNestIdentifier, self).__init__()

        if api_key:
            self.api_key = api_key
        self.start = start
        if os.environ.has_key('HTTP_PROXY'):
            self.proxy = os.environ['HTTP_PROXY']

        self.metadata = None
        self.samples = np.array([])

    @staticmethod
    @interfacedoc
    def id():
        return "echonest_identifier"

    @staticmethod
    @interfacedoc
    def name():
        return "EchoNest Identifier"

    @staticmethod
    @interfacedoc
    def unit():
        return ""

    @downmix_to_mono
    def process(self, frames, eod=False):
        if frames.size:
            self.samples = np.append(self.samples, frames)
        return frames, eod

    def post_process(self):
        if np.count_nonzero(self.samples):
            self.samples = self.samples[self.delay*self.samplerate():]
            print self.samples
            if self.start == -1:
                data = echoprint.codegen(self.samples.astype(np.float))
            else:
                data = echoprint.codegen(self.samples.astype(np.float), int(self.start))

            r = requests.post(self.api_url,
                data={'query': json.dumps(data), 'api_key': self.api_key,
                      'version': data['version']},
                headers={'content-type': 'application/x-www-form-urlencoded'},
                proxies={'http': self.proxy}
            )
            self.metadata = r.json()['response']

        self.samples = np.array([])
