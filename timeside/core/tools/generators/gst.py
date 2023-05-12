#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  7 09:19:37 2014

@author: thomas
"""

import gi
gi.require_version('Gst', '1.0')
gi.require_version('GLib', '2.0')
from gi.repository import GLib, Gst
Gst.init(None)


class NumpySrc:
    def __init__(self, array, samplerate):
        self.appsrc = Gst.ElementFactory.make("appsrc")
        self.pos = 0
        self.samplerate = samplerate
        if array.ndim == 1:
            array.resize((array.shape[0], 1))
        self.length, self.channels = array.shape
        self.array = array.astype("float32")
        self.per_sample = Gst.SECOND // samplerate
        self.fac = self.channels * array.dtype.itemsize
        #self.appsrc.set_property("size", (self.length * self.channels *
        #                                  array.dtype.itemsize))
        self.appsrc.set_property("format", Gst.Format.TIME)
        capstr = """audio/x-raw,format=F32LE,
                    layout=interleaved,
                    rate=%d,
                    channels=%d""" % (self.samplerate,
                                      self.channels)
        self.appsrc.set_property("caps", Gst.caps_from_string(capstr))
        self.appsrc.set_property("stream-type", 0)  # Seekable
        self.appsrc.set_property('block', True)

        self.appsrc.connect("need-data", self.need_data)
        self.appsrc.connect("seek-data", self.seek_data)
        self.appsrc.connect("enough-data", self.enough_data)

    def need_data(self, element, length):
        #length = length // 64
        if self.pos >= self.array.shape[0]:
            element.emit("end-of-stream")
        else:
            avalaible_sample = self.length - self.pos
            if avalaible_sample < length:
                length = avalaible_sample
            array = self.array[self.pos:self.pos+length]
            buf = Gst.Buffer.new_wrapped(array.flatten().tobytes())

            buf.timestamp = self.pos * self.per_sample
            buf.duration = int(length*self.per_sample)
            element.emit("push-buffer", buf)
            self.pos += length

    def seek_data(self, element, npos):
        print ('seek %d' % npos)
        self.pos = npos // self.per_sample
        return True

    def enough_data(self, element):
        print ("----------- enough data ---------------")


class gst_BuildSample(object):
    def __init__(self, sample_array, output_file, gst_audio_encoder):
        if not isinstance(sample_array, SampleArray):
            raise ValueError("array must be a SampleArray subclass")
        self.sample_array = sample_array
        self.samplerate = self.sample_array.samplerate
        self.output_file = output_file
        if not isinstance(gst_audio_encoder, list):
            gst_audio_encoder = [gst_audio_encoder]
        self.gst_audio_encoder = gst_audio_encoder

    def run(self):
        pipeline = Gst.Pipeline("pipeline")
        mainloop = GLib.MainLoop()

        numpy_src = NumpySrc(array=self.sample_array.array,
                             samplerate=self.samplerate)

        converter = Gst.ElementFactory.make('audioconvert', 'converter')

        encoder_muxer = []
        for enc in self.gst_audio_encoder:
            encoder_muxer.append(Gst.ElementFactory.make(enc))

        filesink = Gst.ElementFactory.make('filesink', 'sink')
        filesink.set_property('location', self.output_file)

        pipe_elements = [numpy_src.appsrc, converter]
        pipe_elements.extend(encoder_muxer)
        pipe_elements.append(filesink)

        pipeline.add(*pipe_elements)
        #Gst.Element.link_many(*pipe_elements)
        numpy_src.appsrc.link(converter)
        converter.link(encoder_muxer[0])
        while len(encoder_muxer) > 1:
            next_el = encoder_muxer.pop(0)
            next_el.link(encoder_muxer[0])
        encoder_muxer[0].link(filesink)


        def on_eos(bus, msg):
            pipeline.set_state(Gst.State.NULL)
            mainloop.quit()

        def on_error(bus, msg):
            err, debug_info = msg.parse_error()
            print ("Error received from element %s: %s" % (msg.src.get_name(),
                                                           err))
            print ("Debugging information: %s" % debug_info)
            mainloop.quit()

        pipeline.set_state(Gst.State.PLAYING)
        bus = pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message::eos', on_eos)
        bus.connect("message::error", on_error)

        mainloop.run()
