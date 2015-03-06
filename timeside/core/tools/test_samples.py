#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  7 09:19:37 2014

@author: thomas
"""

from __future__ import division

import pygst
pygst.require("0.10")
import gobject
import gst
import numpy
import scipy.signal.waveforms
import os.path

#import timeside


class NumpySrc:
    def __init__(self, array, samplerate):
        self.appsrc = gst.element_factory_make("appsrc")
        self.pos = 0
        self.samplerate = samplerate
        if array.ndim == 1:
            array.resize((array.shape[0], 1))
        self.length, self.channels = array.shape
        self.array = array.astype("float32")
        self.per_sample = gst.SECOND // samplerate
        self.fac = self.channels * array.dtype.itemsize
        #self.appsrc.set_property("size", (self.length * self.channels *
        #                                  array.dtype.itemsize))
        self.appsrc.set_property("format", gst.FORMAT_TIME)
        capstr = """audio/x-raw-float,
                    width=%d,
                    depth=%d,
                    rate=%d,
                    channels=%d,
                    endianness=(int)1234,
                    signed=true""" % (self.array.dtype.itemsize*8,
                                      self.array.dtype.itemsize*8,
                                      self.samplerate,
                                      self.channels)
        self.appsrc.set_property("caps", gst.caps_from_string(capstr))
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
            buf = gst.Buffer(numpy.getbuffer(array.flatten()))

            buf.timestamp = self.pos * self.per_sample
            buf.duration = int(length*self.per_sample)
            element.emit("push-buffer", buf)
            self.pos += length

    def seek_data(self, element, npos):
        print 'seek %d' % npos
        self.pos = npos // self.per_sample
        return True

    def enough_data(self, element):
        print "----------- enough data ---------------"


class SampleArray(object):
    """Base Class for generating a data sample array"""

    def __init__(self, duration=10, samplerate=44100):
        self.samplerate = int(samplerate)
        self.num_samples = int(numpy.ceil(duration * self.samplerate))
        self.array = NotImplemented

    @property
    def time_samples(self):
        return numpy.arange(0, self.num_samples)

    @property
    def duration(self):
        return self.num_samples / self.samplerate

    def __add__(self, other):
        if not self.samplerate == other.samplerate:
            raise ValueError("Samplerates mismatch")

        sum_ = SampleArray(samplerate=self.samplerate)
        sum_.num_samples = self.num_samples + other.num_samples
        sum_.array = numpy.vstack([self.array, other.array])
        return sum_

    def __and__(self, other):
        if not self.samplerate == other.samplerate:
            raise ValueError("Samplerates mismatch")
        if not self.num_samples == other.num_samples:
            raise ValueError("Number of samples mismatch")

        and_ = SampleArray(samplerate=self.samplerate)
        and_.num_samples = self.num_samples
        and_.array = numpy.hstack([self.array, other.array])
        return and_


class SineArray(SampleArray):
    """Class for generating a Sine array"""
    def __init__(self, frequency=440, duration=10, samplerate=44100,
                 channels=1):
        super(SineArray, self).__init__(duration=duration,
                                        samplerate=samplerate)
        self.frequency = frequency
        self.array = numpy.sin((2 * numpy.pi * self.frequency *
                               self.time_samples / self.samplerate))
        self.array.resize(self.num_samples, 1)


class SweepArray(SampleArray):
    """Class for generating a Sweep array"""
    def __init__(self, f0=20, f1=None, duration=10, samplerate=44100,
                 method='logarithmic'):
        super(SweepArray, self).__init__(duration=duration,
                                         samplerate=samplerate)

        self.f0 = f0 / samplerate
        if f1 is None:
            self.f1 = 0.5
        else:
            self.f1 = f1 / samplerate
        self.method = method
        self.array = scipy.signal.waveforms.chirp(t=self.time_samples,
                                                  f0=self.f0,
                                                  t1=self.time_samples[-1],
                                                  f1=self.f1,
                                                  method=self.method)
        self.array.resize(self.num_samples, 1)


class WhiteNoiseArray(SampleArray):
    """Class for generating a white noise array"""
    def __init__(self, duration=10, samplerate=44100):
        super(WhiteNoiseArray, self).__init__(duration=duration,
                                              samplerate=samplerate)
        array = numpy.random.randn(self.num_samples, 1)
        self.array = array / abs(array).max()


class SilenceArray(SampleArray):
    """Class for generating a silence"""
    def __init__(self, duration=10, samplerate=44100):
        super(SilenceArray, self).__init__(duration=duration,
                                           samplerate=samplerate)

        self.array = numpy.zeros((self.num_samples, 1))


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
        pipeline = gst.Pipeline("pipeline")
        gobject.threads_init()
        mainloop = gobject.MainLoop()

        numpy_src = NumpySrc(array=self.sample_array.array,
                             samplerate=self.samplerate)

        converter = gst.element_factory_make('audioconvert', 'converter')

        encoder_muxer = []
        for enc in self.gst_audio_encoder:
            encoder_muxer.append(gst.element_factory_make(enc))

        filesink = gst.element_factory_make('filesink', 'sink')
        filesink.set_property('location', self.output_file)

        pipe_elements = [numpy_src.appsrc, converter]
        pipe_elements.extend(encoder_muxer)
        pipe_elements.append(filesink)

        pipeline.add(*pipe_elements)
        gst.element_link_many(*pipe_elements)

        def _on_new_pad(self, source, pad, target_pad):
            print 'on_new_pad'
            if not pad.is_linked():
                if target_pad.is_linked():
                    target_pad.get_peer().unlink(target_pad)
                pad.link(target_pad)

        def on_eos(bus, msg):
            pipeline.set_state(gst.STATE_NULL)
            mainloop.quit()

        def on_error(bus, msg):
            err, debug_info = msg.parse_error()
            print ("Error received from element %s: %s" % (msg.src.get_name(),
                                                           err))
            print ("Debugging information: %s" % debug_info)
            mainloop.quit()

        pipeline.set_state(gst.STATE_PLAYING)
        bus = pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message::eos', on_eos)
        bus.connect("message::error", on_error)

        mainloop.run()


def generate_sample_file(filename, samples_dir, gst_audio_encoder,
                         sample_array, overwrite=False):
    sample_file = os.path.join(samples_dir, filename)

    if overwrite or not os.path.exists(sample_file):
            gst_builder = gst_BuildSample(sample_array=sample_array,
                                          output_file=sample_file,
                                          gst_audio_encoder=gst_audio_encoder)
            gst_builder.run()
    return sample_file


def generateSamples(overwrite=False, samples_dir=None):
    if not samples_dir:
        from timeside import __file__ as ts_file
        ts_path = os.path.split(os.path.abspath(ts_file))[0]
        tests_dir = os.path.abspath(os.path.join(ts_path, '../tests'))
        if os.path.isdir(tests_dir):
            samples_dir = os.path.abspath(os.path.join(tests_dir, 'samples'))
            if not os.path.isdir(samples_dir):
                os.makedirs(samples_dir)
        else:
            import tempfile
            samples_dir = tempfile.mkdtemp(suffix="ts_samples")
    else:
        if not os.path.isdir(samples_dir):
            os.makedirs(samples_dir)

    samples = dict()

    # --------- Sweeps ---------
    # sweep 44100 mono wav
    filename = 'sweep_mono.wav'
    samplerate = 44100
    gst_audio_encoder = 'wavenc'
    sweep_mono = SweepArray(duration=8, samplerate=samplerate)
    sample_file = generate_sample_file(filename, samples_dir,
                                       gst_audio_encoder,
                                       sample_array=sweep_mono,
                                       overwrite=overwrite)
    samples.update({filename: sample_file})

    # sweep 44100 stereo wav
    sweep_stereo = sweep_mono & sweep_mono
    filename = 'sweep.wav'
    gst_audio_encoder = 'wavenc'
    sweep_mono = SweepArray(duration=8, samplerate=samplerate)
    sample_file = generate_sample_file(filename, samples_dir,
                                       gst_audio_encoder,
                                       sample_array=sweep_stereo,
                                       overwrite=overwrite)
    samples.update({filename: sample_file})

   # sweep 44100 stereo mp3
    filename = 'sweep.mp3'
    gst_audio_encoder = ['lamemp3enc', 'xingmux', 'id3v2mux']
    sweep_mono = SweepArray(duration=8, samplerate=samplerate)
    sample_file = generate_sample_file(filename, samples_dir,
                                       gst_audio_encoder,
                                       sample_array=sweep_stereo,
                                       overwrite=overwrite)
    samples.update({filename: sample_file})

   # sweep 44100 stereo flac
    filename = 'sweep.flac'
    gst_audio_encoder = 'flacenc'
    sweep_mono = SweepArray(duration=8, samplerate=samplerate)
    sample_file = generate_sample_file(filename, samples_dir,
                                       gst_audio_encoder,
                                       sample_array=sweep_stereo,
                                       overwrite=overwrite)
    samples.update({filename: sample_file})

   # sweep 44100 stereo ogg
    filename = 'sweep.ogg'
    gst_audio_encoder = ['vorbisenc', 'oggmux']
    sweep_mono = SweepArray(duration=8, samplerate=samplerate)
    sample_file = generate_sample_file(filename, samples_dir,
                                       gst_audio_encoder,
                                       sample_array=sweep_stereo,
                                       overwrite=overwrite)
    samples.update({filename: sample_file})

    # sweep 32000 stereo wav
    samplerate = 32000
    sweep_mono = SweepArray(duration=8, samplerate=samplerate)
    sweep_stereo = sweep_mono & sweep_mono

    filename = 'sweep_32000.wav'
    gst_audio_encoder = 'wavenc'
    sweep_mono = SweepArray(duration=8, samplerate=samplerate)
    sample_file = generate_sample_file(filename, samples_dir,
                                       gst_audio_encoder,
                                       sample_array=sweep_stereo,
                                       overwrite=overwrite)
    samples.update({filename: sample_file})

    # --------- Sines ---------
    # sine at 440Hz,  44100 mono wav
    filename = 'sine440Hz_mono.wav'
    samplerate = 44100
    gst_audio_encoder = 'wavenc'
    sweep_mono = SineArray(duration=8, samplerate=samplerate, frequency=440)
    sample_file = generate_sample_file(filename, samples_dir,
                                       gst_audio_encoder,
                                       sample_array=sweep_mono,
                                       overwrite=overwrite)
    samples.update({filename: sample_file})

    # Short 1s sine at 440Hz,  44100 mono wav
    filename = 'sine440Hz_mono_1s.wav'
    samplerate = 44100
    gst_audio_encoder = 'wavenc'
    sweep_mono = SineArray(duration=1, samplerate=samplerate, frequency=440)
    sample_file = generate_sample_file(filename, samples_dir,
                                       gst_audio_encoder,
                                       sample_array=sweep_mono,
                                       overwrite=overwrite)
    samples.update({filename: sample_file})

    # sine at 440Hz,  44100 stereo wav
    filename = 'sine440Hz.wav'
    sweep_stereo = sweep_mono & sweep_mono
    gst_audio_encoder = 'wavenc'
    sweep_mono = SineArray(duration=8, samplerate=samplerate, frequency=440)
    sample_file = generate_sample_file(filename, samples_dir,
                                       gst_audio_encoder,
                                       sample_array=sweep_stereo,
                                       overwrite=overwrite)
    samples.update({filename: sample_file})

    # sine at 440Hz,  44100 stereo mp3
    filename = 'sine440Hz.mp3'
    gst_audio_encoder = ['lamemp3enc', 'xingmux', 'id3v2mux']
    sweep_mono = SineArray(duration=8, samplerate=samplerate, frequency=440)
    sample_file = generate_sample_file(filename, samples_dir,
                                       gst_audio_encoder,
                                       sample_array=sweep_stereo,
                                       overwrite=overwrite)
    samples.update({filename: sample_file})

    # sine at 440Hz,  44100 stereo ogg
    filename = 'sine440Hz.ogg'
    gst_audio_encoder = ['vorbisenc', 'oggmux']
    sweep_mono = SineArray(duration=8, samplerate=samplerate, frequency=440)
    sample_file = generate_sample_file(filename, samples_dir,
                                       gst_audio_encoder,
                                       sample_array=sweep_stereo,
                                       overwrite=overwrite)
    samples.update({filename: sample_file})

    # --------- Equal tempered scale ---------
    filename = 'C4_scale.wav'
    samplerate = 44100
    f_C4 = 261.63
    f_D4 = 293.66
    f_E4 = 329.63
    f_F4 = 349.23
    f_G4 = 392.00
    f_A4 = 440.00
    f_B4 = 493.88
    f_C5 = 523.25
    sineC4 = SineArray(duration=1, samplerate=samplerate, frequency=f_C4)
    sineD4 = SineArray(duration=1, samplerate=samplerate, frequency=f_D4)
    sineE4 = SineArray(duration=1, samplerate=samplerate, frequency=f_E4)
    sineF4 = SineArray(duration=1, samplerate=samplerate, frequency=f_F4)
    sineG4 = SineArray(duration=1, samplerate=samplerate, frequency=f_G4)
    sineA4 = SineArray(duration=1, samplerate=samplerate, frequency=f_A4)
    sineB4 = SineArray(duration=1, samplerate=samplerate, frequency=f_B4)
    sineC5 = SineArray(duration=1, samplerate=samplerate, frequency=f_C5)

    silence = SilenceArray(duration=0.2, samplerate=samplerate)

    scale = (sineC4 + silence + sineD4 + silence + sineE4 + silence +
             sineF4 + silence + sineG4 + silence + sineA4 + silence +
             sineB4 + silence + sineC5)

    gst_audio_encoder = 'wavenc'
    sample_file = generate_sample_file(filename, samples_dir,
                                       gst_audio_encoder,
                                       sample_array=scale,
                                       overwrite=overwrite)
    samples.update({filename: sample_file})

    # --------- White noise ---------
    # white noise - 44100Hz mono
    filename = 'white_noise_mono.wav'
    samplerate = 44100
    noise = WhiteNoiseArray(duration=8, samplerate=samplerate)
    gst_audio_encoder = 'wavenc'
    sample_file = generate_sample_file(filename, samples_dir,
                                       gst_audio_encoder,
                                       sample_array=noise,
                                       overwrite=overwrite)
    samples.update({filename: sample_file})

    # white noise - 44100Hz stereo
    filename = 'white_noise.wav'
    samplerate = 44100
    noise = WhiteNoiseArray(duration=8, samplerate=samplerate)
    noise_stereo = noise & noise
    gst_audio_encoder = 'wavenc'
    sample_file = generate_sample_file(filename, samples_dir,
                                       gst_audio_encoder,
                                       sample_array=noise_stereo,
                                       overwrite=overwrite)
    samples.update({filename: sample_file})

    # white noise - 32000Hz stereo
    filename = 'white_noise_32000.wav'
    samplerate = 32000
    noise = WhiteNoiseArray(duration=8, samplerate=samplerate)
    noise_stereo = noise & noise
    gst_audio_encoder = 'wavenc'
    sample_file = generate_sample_file(filename, samples_dir,
                                       gst_audio_encoder,
                                       sample_array=noise_stereo,
                                       overwrite=overwrite)
    samples.update({filename: sample_file})

    return samples


samples = generateSamples()


if __name__ == '__main__':
    generateSamples()
