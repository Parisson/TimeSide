from numpy import getbuffer

import pygst
pygst.require('0.10')
import gst
import gobject
gobject.threads_init()

def numpy_array_to_gst_buffer(frames):
    """ gstreamer buffer to numpy array conversion """
    buf = gst.Buffer(getbuffer(frames.astype("float32")))
    return buf

