#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2007-2013 Parisson
# Copyright (c) 2007 Olivier Guilyardi <olivier@samalyse.com>
# Copyright (c) 2007-2013 Guillaume Pellerin <pellerin@parisson.com>
# Copyright (c) 2010-2013 Paul Brossier <piem@piem.org>
#
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
# Paul Brossier <piem@piem.org>
# Guillaume Pellerin <yomguy@parisson.com>
# Thomas Fillon <thomas@parisson.com>

from __future__ import division

from timeside.core.decoder import Decoder, IDecoder, interfacedoc, implements
from timeside.core.tools.gstutils import MainloopThread, gobject
from timeside.plugins.decoder.file import FileDecoder
import Queue
import threading

from gst import _gst as gst

GST_APPSINK_MAX_BUFFERS = 10
QUEUE_SIZE = 10

#  TODO:
# check if a soundcard device is available
# alsasrc = gst.element_factory_make("alsasrc", "alsasrc")
# alsasrc.probe_get_values_name('device')
# ['hw:0,0']


class LiveDecoder(FileDecoder):
    """Live source Decoder based on Gstreamer
   capturing audio from alsasrc

    Construct a new LiveDecoder capturing audio from alsasrc

    Parameters
    ----------
    num_buffers : int, optional
        Number of buffers to output before sending End Of Stream signal
        (-1 = unlimited).
        (Allowed values: >= -1, Default value: -1)

    input_src : str, optional
        Gstreamer source element
        default to 'alsasrc'
        possible values :  'autoaudiosrc', 'alsasrc', 'osssrc'

    Examples
    --------

    >>> import timeside

    >>> from timeside.core import get_processor
    >>> live_decoder = get_processor('live_decoder')(num_buffers=5)
    >>> waveform = get_processor('waveform_analyzer')()
    >>> mp3_encoder = timeside.plugins.encoder.mp3.Mp3Encoder('/tmp/test_live.mp3',
    ...                                               overwrite=True)
    >>> pipe = (live_decoder | waveform | mp3_encoder)
    >>> pipe.run()  # doctest: +SKIP
    >>> # Show the audio as captured by the decoder
    >>> import matplotlib.pyplot as plt # doctest: +SKIP
    >>> plt.plot(a.results['waveform_analyzer'].time, # doctest: +SKIP
             a.results['waveform_analyzer'].data) # doctest: +SKIP
    >>> plt.show() # doctest: +SKIP

        """
    implements(IDecoder)

    # IProcessor methods

    @staticmethod
    @interfacedoc
    def id():
        return "live_decoder"

    def __init__(self, num_buffers=-1, input_src='alsasrc'):

        super(Decoder, self).__init__()
        self.num_buffers = num_buffers
        self.uri = None
        self.uri_start = 0
        self.uri_duration = None
        self.is_segment = False
        self.input_src = input_src
        self._sha1 = ''

    def setup(self, channels=None, samplerate=None, blocksize=None):

        self.eod = False
        self.last_buffer = None

        # a lock to wait wait for gstreamer thread to be ready
        self.discovered_cond = threading.Condition(threading.Lock())
        self.discovered = False

        # the output data format we want
        if blocksize:
            self.output_blocksize = blocksize
        if samplerate:
            self.output_samplerate = int(samplerate)
        if channels:
            self.output_channels = int(channels)

        # Create the pipe with standard Gstreamer uridecodbin
        self.pipe = '''%s num-buffers=%d name=src
                       ! audioconvert name=audioconvert
                       ! audioresample
                       ! appsink name=sink sync=False async=True
                       ''' % (self.input_src, self.num_buffers)

        self.pipeline = gst.parse_launch(self.pipe)

        if self.output_channels:
            caps_channels = int(self.output_channels)
        else:
            caps_channels = "[ 1, 2 ]"
        if self.output_samplerate:
            caps_samplerate = int(self.output_samplerate)
        else:
            caps_samplerate = "{ 8000, 11025, 12000, 16000, 22050, 24000, 32000, 44100, 48000, 96000 }"
        sink_caps = gst.Caps("""audio/x-raw-float,
            endianness=(int)1234,
            channels=(int)%s,
            width=(int)32,
            rate=(int)%s""" % (caps_channels, caps_samplerate))

        self.src = self.pipeline.get_by_name('src')
        self.conv = self.pipeline.get_by_name('audioconvert')
        self.conv.get_pad("sink").connect("notify::caps", self._notify_caps_cb)

        self.sink = self.pipeline.get_by_name('sink')
        self.sink.set_property("caps", sink_caps)
        self.sink.set_property('max-buffers', GST_APPSINK_MAX_BUFFERS)
        self.sink.set_property("drop", False)
        self.sink.set_property('emit-signals', True)
        self.sink.connect("new-buffer", self._on_new_buffer_cb)

        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message', self._on_message_cb)

        self.queue = Queue.Queue(QUEUE_SIZE)

        self.mainloop = gobject.MainLoop()
        self.mainloopthread = MainloopThread(self.mainloop)
        self.mainloopthread.start()
        #self.mainloopthread = get_loop_thread()
        ##self.mainloop = self.mainloopthread.mainloop

        # start pipeline
        self.pipeline.set_state(gst.STATE_PLAYING)

        self.discovered_cond.acquire()
        while not self.discovered:
            # print 'waiting'
            self.discovered_cond.wait()
        self.discovered_cond.release()

        if not hasattr(self, 'input_samplerate'):
            if hasattr(self, 'error_msg'):
                raise IOError(self.error_msg)
            else:
                raise IOError('no known audio stream found')

    @interfacedoc
    def process(self):
        buf = self.queue.get()
        if buf == gst.MESSAGE_EOS:
            return self.last_buffer, True

        frames, eod = buf
        return frames, eod

    def release(self):
        # TODO : check if stack support is needed here
        #if self.stack:
        #    self.stack = False
        #    self.from_stack = True
        pass

    # IDecoder methods

if __name__ == "__main__":
    import doctest
    import timeside
    doctest.testmod(timeside.plugins.decoder.live, verbose=True)
