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
#          Guilaume Pellerin <yomguy@parisson.com>

from timeside.core import Processor, implements, interfacedoc
from timeside.api import IDecoder
from timeside.encoder.gstutils import *

import Queue

GST_APPSINK_MAX_BUFFERS = 10
QUEUE_SIZE = 10

class FileDecoder(Processor):
    """ gstreamer-based decoder """
    implements(IDecoder)

    mimetype = ''
    output_blocksize  = 8*1024
    output_samplerate = 44100
    output_channels   = 1

    pipeline          = None
    mainloopthread    = None
    read_error        = None

    # IProcessor methods

    @staticmethod
    @interfacedoc
    def id():
        return "gstreamerdec"

    def __init__(self, uri):
        # is this a file?
        import os.path
        if os.path.exists(uri):
            # get the absolute path
            uri = os.path.abspath(uri)
            # and make a uri of it
            from urllib import quote
            self.uri = 'file://'+quote(uri)
        else:
            self.uri = uri

    def setup(self, channels = None, samplerate = None, blocksize = None):
        # the output data format we want
        if blocksize:   self.output_blocksize  = blocksize
        if samplerate:  self.output_samplerate = int(samplerate)
        if channels:    self.output_channels   = int(channels)

        uri = self.uri

        self.pipe = ''' uridecodebin name=uridecodebin uri=%(uri)s
                  ! audioconvert name=audioconvert
                  ! audioresample
                  ! appsink name=sink sync=False async=True
                  ''' % locals()
        self.pipeline = gst.parse_launch(self.pipe)

        sink_caps = gst.Caps("""audio/x-raw-float,
            endianness=(int)1234,
            channels=(int)%s,
            width=(int)32,
            rate=(int)%d""" % (int(self.output_channels), int(self.output_samplerate)))

        self.decodebin = self.pipeline.get_by_name('uridecodebin')
        self.decodebin.connect("pad-added", self._pad_added_cb)
        self.decodebin.connect("no-more-pads", self._no_more_pads_cb)
        self.decodebin.connect("unknown-type", self._unknown_type_cb)

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

        self._pad_found = False

        # start pipeline
        self.pipeline.set_state(gst.STATE_PLAYING)

        if self.read_error:
            self.release()
            raise self.read_error

    def _pad_added_cb(self, decodebin, pad):
        caps = pad.get_caps()
        if caps.to_string().startswith('audio'):
            if not self.conv.get_pad('sink').is_linked():
                self._pad_found = True
                pad.link(self.conv.get_pad('sink'))

    def _no_more_pads_cb(self, decodebin):
        self.pipeline.info("no more pads")
        if not self._pad_found:
            self.read_exc = Exception("no audio stream found")

    def _unknown_type_cb(self, decodebin, pad, caps):
        self.pipeline.debug("unknown type : %s" % caps.to_string())
        if not caps.to_string().startswith('audio'):
            return
        self.read_error = Exception("no known audio stream found")

    def _notify_caps_cb(self, pad, args):
        caps = pad.get_negotiated_caps()
        if not caps:
            pad.info("no negotiated caps available")
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
            self.input_channels = caps[0]["channels"]
            self.input_duration = length / 1.e9
            self.input_totalframes = int(self.input_duration * self.input_samplerate)
            if "x-raw-float" in caps.to_string():
                self.input_width = caps[0]["width"]
            else:
                self.input_width = caps[0]["depth"]

    def _on_message_cb(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.pipeline.set_state(gst.STATE_NULL)
            self.queue.put(gst.MESSAGE_EOS)
            self.mainloop.quit()
        elif t == gst.MESSAGE_ERROR:
            self.pipeline.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            self.mainloop.quit()
            print "Error: %s" % err, debug
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
            self.queue.put( [new_block, False ] )

    @interfacedoc
    def process(self, frames = None, eod = False):
        buf = self.queue.get()
        if buf == gst.MESSAGE_EOS:
            return self.last_buffer, True
        frames, eod = buf
        return frames, eod

    @interfacedoc
    def channels(self):
        return  self.output_channels

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
        if self.pipeline: self.pipeline.set_state(gst.STATE_NULL)
        if self.mainloopthread: self.mainloopthread.join()

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

