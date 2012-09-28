from timeside.core import Processor, implements, interfacedoc
from timeside.api import IEncoder

from numpy import array, getbuffer, frombuffer

import pygst
pygst.require('0.10')
import gst
import gobject

gobject.threads_init()

def numpy_array_to_gst_buffer(frames):
    """ gstreamer buffer to numpy array conversion """
    buf = gst.Buffer(getbuffer(frames.astype("float32")))
    return buf

def gst_buffer_to_numpy_array(buf, chan):
    """ gstreamer buffer to numpy array conversion """
    samples = frombuffer(buf.data, dtype='float32')
    samples.resize([len(samples)/chan, chan])
    return samples

class GstEncoder(Processor):

    def release(self):
        while self.bus.have_pending():
          self.bus.pop()

    def __del__(self):
        self.release()

    def start_pipeline(self, channels, samplerate):
        self.pipeline = gst.parse_launch(self.pipe)
        # store a pointer to appsrc in our encoder object
        self.src = self.pipeline.get_by_name('src')
        # store a pointer to appsink in our encoder object
        self.app = self.pipeline.get_by_name('app')

        srccaps = gst.Caps("""audio/x-raw-float,
            endianness=(int)1234,
            channels=(int)%s,
            width=(int)32,
            rate=(int)%d""" % (int(channels), int(samplerate)))
        self.src.set_property("caps", srccaps)
        self.src.set_property('emit-signals', True)

        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect("message", self.on_message)

        # start pipeline
        self.pipeline.set_state(gst.STATE_PLAYING)

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.pipeline.set_state(gst.STATE_NULL)
        elif t == gst.MESSAGE_ERROR:
            self.pipeline.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            print "Error: %s" % err, debug

    def process(self, frames, eod=False):
        self.eod = eod
        buf = numpy_array_to_gst_buffer(frames)
        self.src.emit('push-buffer', buf)
        if self.eod:
            self.src.emit('end-of-stream')
        if self.streaming:
            self.chunk = self.app.emit('pull-buffer')
        return frames, eod
