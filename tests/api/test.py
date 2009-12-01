from timeside.tests.api import examples
import os

source=os.path.dirname(__file__) + "../samples/sweep_source.wav"

Decoder = examples.AudiolabDecoder
print "Creating decoder with id=%s for: %s" % (Decoder.id(), source)
decoder = Decoder(source)
nchannels, samplerate = decoder.output_format()
print "Stats: duration=%f, nframes=%d, nchannels=%d, samplerate=%d, resolution=%d" % (
        decoder.duration(), decoder.nframes(), nchannels, samplerate, decoder.resolution())

analyzer = examples.MaxLevelAnalyzer()
analyzer.set_input_format(nchannels, samplerate)

while True:
    frames = decoder.process()
    analyzer.process(frames)
    if len(frames) < decoder.buffersize():
        break

max_level = analyzer.result()
print "Max level: %f" % max_level

destination = "normalized.wav"
Encoder = examples.WavEncoder
print "Creating encoder with id=%s for: %s" % (Encoder.id(), destination)
encoder = Encoder(destination)
decoder = Decoder(source)

nchannels, samplerate = decoder.output_format()
encoder.set_input_format(nchannels, samplerate)

gain = 1
if max_level > 0:
    gain = 0.9 / max_level

effect = examples.GainEffect(gain)

print "Applying effect id=%s with gain=%f" % (effect.id(), gain)

while True:
    frames = decoder.process()
    encoder.process(effect.process(frames))
    if len(frames) < decoder.buffersize():
        break

