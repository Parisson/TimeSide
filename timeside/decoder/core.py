#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2007-2011 Parisson
# Copyright (c) 2007 Olivier Guilyardi <olivier@samalyse.com>
# Copyright (c) 2007-2011 Guillaume Pellerin <pellerin@parisson.com>
# Copyright (c) 2010-2011 Paul Brossier <piem@piem.org>
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

# Authors: Paul Brossier <piem@piem.org>
# Guillaume Pellerin <yomguy@parisson.com>

from timeside.core import Processor, implements, interfacedoc
from timeside.api import IDecoder
from timeside.tools import *

import Queue
from gst import _gst as gst
from numpy import int64, uint64


GST_APPSINK_MAX_BUFFERS = 10
QUEUE_SIZE = 10
GST_DISCOVER_TIMEOUT = 5000000000L


class FileDecoder(Processor):
    """ gstreamer-based decoder """
    implements(IDecoder)

    mimetype = ''
    output_blocksize  = 8*1024
    output_samplerate = None
    output_channels   = None

    pipeline          = None
    mainloopthread    = None

    # IProcessor methods

    @staticmethod
    @interfacedoc
    def id():
        return "gst_dec"

    def __init__(self, uri, start = 0, duration = None):
        '''
            Construct a new FileDecoder

            Parameters
            ----------
            uri: uri of the media
            start : float
                start time of the segment in seconds
            duration : float
                duration of the segment in seconds
        '''
        super(FileDecoder, self).__init__()

        # is this a file?
        import os.path
        if os.path.exists(uri):
            # get the absolute path
            uri = os.path.abspath(uri)
            # and make a uri of it
            from urllib import quote
            self.uri = 'file://' + quote(uri)
        elif '://' in uri:
            self.uri = uri
        else:
            raise IOError('File not found!')

        self.uri_start = float(start)
        if duration:
            self.uri_duration = float(duration)
        else:
            self.uri_duration = duration

        if start==0 and duration is None:
            self.is_segment = False
        else:
            self.is_segment = True

    def set_uri_default_duration(self):
        # Set the duration from the length of the file
        from gst.pbutils import Discoverer
        from glib import GError
        #import gobject
        uri_discoverer = Discoverer(GST_DISCOVER_TIMEOUT)
        try:
            uri_info = uri_discoverer.discover_uri(self.uri)
        except  GError as e:
            raise IOError(e)
        self.uri_duration = (uri_info.get_duration() / float(gst.SECOND) -
                            self.uri_start)

    def setup(self, channels=None, samplerate=None, blocksize=None):

        if self.uri_duration is None:
            self.set_uri_default_duration()

        # a lock to wait wait for gstreamer thread to be ready
        import threading
        self.discovered_cond = threading.Condition(threading.Lock())
        self.discovered = False

        # the output data format we want
        if blocksize:
            self.output_blocksize = blocksize
        if samplerate:
            self.output_samplerate = int(samplerate)
        if channels:
            self.output_channels = int(channels)

        if self.is_segment:
            # Create the pipe with Gnonlin gnlurisource
            self.pipe = ''' gnlurisource uri={uri}
                            start=0
                            duration={uri_duration}
                            media-start={uri_start}
                            media-duration={uri_duration}
                            ! audioconvert name=audioconvert
                            ! audioresample
                            ! appsink name=sink sync=False async=True
                            '''.format(uri = self.uri,
                                       uri_start = uint64(round(self.uri_start * gst.SECOND)),
                                       uri_duration = int64(round(self.uri_duration * gst.SECOND)))
                                       # convert uri_start and uri_duration to nanoseconds
        else:
            # Create the pipe with standard Gstreamer uridecodbin
            self.pipe = ''' uridecodebin name=uridecodebin uri={uri}
                           ! audioconvert name=audioconvert
                           ! audioresample
                           ! appsink name=sink sync=False async=True
                           '''.format(uri = self.uri)

        self.pipeline = gst.parse_launch(self.pipe)

        if self.output_channels:
            caps_channels = int(self.output_channels)
        else:
            caps_channels = "[ 1, 2 ]"
        if self.output_samplerate:
            caps_samplerate = int(self.output_samplerate)
        else:
            caps_samplerate = "{ 8000, 11025, 12000, 16000, 22050, 24000, 32000, 44100, 48000 }"
        sink_caps = gst.Caps("""audio/x-raw-float,
            endianness=(int)1234,
            channels=(int)%s,
            width=(int)32,
            rate=(int)%s""" % (caps_channels, caps_samplerate))

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

        import threading

        class MainloopThread(threading.Thread):
            def __init__(self, mainloop):
                threading.Thread.__init__(self)
                self.mainloop = mainloop

            def run(self):
                self.mainloop.run()
        self.mainloop = gobject.MainLoop()
        self.mainloopthread = MainloopThread(self.mainloop)
        self.mainloopthread.start()
        #self.mainloopthread = get_loop_thread()
        ##self.mainloop = self.mainloopthread.mainloop

        self.eod = False

        self.last_buffer = None

        # start pipeline
        self.pipeline.set_state(gst.STATE_PLAYING)

        self.discovered_cond.acquire()
        while not self.discovered:
            #print 'waiting'
            self.discovered_cond.wait()
        self.discovered_cond.release()

        if not hasattr(self, 'input_samplerate'):
            if hasattr(self, 'error_msg'):
                raise IOError(self.error_msg)
            else:
                raise IOError('no known audio stream found')

    def _notify_caps_cb(self, pad, args):
        self.discovered_cond.acquire()

        caps = pad.get_negotiated_caps()
        if not caps:
            pad.info("no negotiated caps available")
            self.discovered = True
            self.discovered_cond.notify()
            self.discovered_cond.release()
            return
        # the caps are fixed
        # We now get the total length of that stream
        q = gst.query_new_duration(gst.FORMAT_TIME)
        pad.info("sending duration query")
        if pad.get_peer().query(q):
            format, length = q.parse_duration()
            if format == gst.FORMAT_TIME:
                pad.info("got duration (time) : %s" % (gst.TIME_ARGS(length),))
            else:
                pad.info("got duration : %d [format:%d]" % (length, format))
        else:
            length = -1
            gst.warning("duration query failed")

        # We store the caps and length in the proper location
        if "audio" in caps.to_string():
            self.input_samplerate = caps[0]["rate"]
            if not self.output_samplerate:
                self.output_samplerate = self.input_samplerate
            self.input_channels = caps[0]["channels"]
            if not self.output_channels:
                self.output_channels = self.input_channels
            self.input_duration = length / 1.e9
            self.input_totalframes = int(self.input_duration * self.input_samplerate)
            if "x-raw-float" in caps.to_string():
                self.input_width = caps[0]["width"]
            else:
                self.input_width = caps[0]["depth"]

        self.discovered = True
        self.discovered_cond.notify()
        self.discovered_cond.release()

    def _on_message_cb(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.queue.put(gst.MESSAGE_EOS)
            self.pipeline.set_state(gst.STATE_NULL)
            self.mainloop.quit()
        elif t == gst.MESSAGE_ERROR:
            self.pipeline.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            self.discovered_cond.acquire()
            self.discovered = True
            self.mainloop.quit()
            self.error_msg = "Error: %s" % err, debug
            self.discovered_cond.notify()
            self.discovered_cond.release()
        elif t == gst.MESSAGE_TAG:
            # TODO
            # msg.parse_tags()
            pass

    def _on_new_buffer_cb(self, sink):
        from numpy import concatenate
        buf = sink.emit('pull-buffer')
        new_array = gst_buffer_to_numpy_array(buf, self.output_channels)
        #print 'processing new buffer', new_array.shape
        if self.last_buffer is None:
            self.last_buffer = new_array
        else:
            self.last_buffer = concatenate((self.last_buffer, new_array), axis=0)
        while self.last_buffer.shape[0] >= self.output_blocksize:
            new_block = self.last_buffer[:self.output_blocksize]
            self.last_buffer = self.last_buffer[self.output_blocksize:]
            #print 'queueing', new_block.shape, 'remaining', self.last_buffer.shape
            self.queue.put([new_block, False])

    @interfacedoc
    def process(self, frames=None, eod=False):
        buf = self.queue.get()
        if buf == gst.MESSAGE_EOS:
            return self.last_buffer, True
        frames, eod = buf
        return frames, eod

    @interfacedoc
    def channels(self):
        return self.output_channels

    @interfacedoc
    def samplerate(self):
        return self.output_samplerate

    @interfacedoc
    def blocksize(self):
        return self.output_blocksize

    @interfacedoc
    def totalframes(self):
        if self.input_samplerate == self.output_samplerate:
            return self.input_totalframes
        else:
            ratio = float(self.output_samplerate) / self.input_samplerate
            return int(self.input_totalframes * ratio)

    @interfacedoc
    def release(self):
        pass

    @interfacedoc
    def mediainfo(self):
        return dict(uri=self.uri,
                    duration=self.uri_duration,
                    start=self.uri_start,
                    is_segment=self.is_segment,
                    samplerate=self.input_samplerate)

    def __del__(self):
        self.release()

    ## IDecoder methods

    @interfacedoc
    def format(self):
        # TODO check
        if self.mimetype == 'application/x-id3':
            self.mimetype = 'audio/mpeg'
        return self.mimetype

    @interfacedoc
    def encoding(self):
        # TODO check
        return self.mimetype.split('/')[-1]

    @interfacedoc
    def resolution(self):
        # TODO check: width or depth?
        return self.audiowidth

    @interfacedoc
    def metadata(self):
        # TODO check
        return self.tags
