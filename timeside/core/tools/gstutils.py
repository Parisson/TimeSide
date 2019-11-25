from numpy import getbuffer, frombuffer

import gi
gi.require_version('Gst', '1.0')
gi.require_version('GLib', '2.0')
gi.require_version('GObject', '2.0')
from gi.repository import GLib, Gobject, Gst
Gst.init(None)

import threading


def numpy_array_to_gst_buffer(frames, chunk_size, num_samples, sample_rate):
    from gst import Buffer
    """ gstreamer buffer to numpy array conversion """
    buf = Buffer(getbuffer(frames.astype("float32")))
    # Set its timestamp and duration
    buf.timestamp = gst.util_uint64_scale(num_samples, gst.SECOND, sample_rate)
    buf.duration = gst.util_uint64_scale(chunk_size, gst.SECOND, sample_rate)
    return buf


def gst_buffer_to_numpy_array(buf, chan):
    """ gstreamer buffer to numpy array conversion """
    samples = frombuffer(buf.data, dtype='float32').reshape((-1, chan))
    return samples


class MainloopThread(threading.Thread):

    def __init__(self, mainloop):
        threading.Thread.__init__(self)
        self.mainloop = mainloop

    def run(self):
        self.mainloop.run()
