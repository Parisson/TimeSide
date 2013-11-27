from numpy import array, getbuffer, frombuffer

import pygst
pygst.require('0.10')
import gst
import gobject
gobject.threads_init()


def numpy_array_to_gst_buffer(frames, CHUNK_SIZE, num_samples, SAMPLE_RATE):
    from gst import Buffer
    """ gstreamer buffer to numpy array conversion """
    buf = Buffer(getbuffer(frames.astype("float32")))
    #Set its timestamp and duration
    buf.timestamp = gst.util_uint64_scale(num_samples, gst.SECOND, SAMPLE_RATE)
    buf.duration = gst.util_uint64_scale(CHUNK_SIZE, gst.SECOND, SAMPLE_RATE)

    return buf


def gst_buffer_to_numpy_array(buf, chan):
    """ gstreamer buffer to numpy array conversion """
    samples = frombuffer(buf.data, dtype='float32')
    samples.resize([len(samples)/chan, chan])
    return samples
