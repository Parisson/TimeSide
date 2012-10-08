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
