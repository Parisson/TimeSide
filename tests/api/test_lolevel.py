from timeside.tests.api import examples

import sys
if len(sys.argv) > 1:
    source = sys.argv[1]
else:
    import os.path
    source= os.path.join (os.path.dirname(__file__),  "../samples/guitar.wav")

Decoder = examples.FileDecoder
print "Creating decoder with id=%s for: %s" % (Decoder.id(), source)
decoder    = Decoder(source)
analyzer = examples.MaxLevel()
decoder.setup()
nchannels  = decoder.channels()
samplerate = decoder.samplerate()
nframes = decoder.nframes()
analyzer.setup(nchannels, samplerate)

print "Stats: duration=%f, nframes=%d, nchannels=%d, samplerate=%d, resolution=%d" % (
        nframes / float(samplerate), nframes, nchannels, samplerate, decoder.resolution())

while True:
    frames, eod = decoder.process()
    analyzer.process(frames, eod)
    if eod:
        break

max_level = analyzer.result()
print "Max level: %f" % max_level

destination = "normalized.wav"
Encoder = examples.WavEncoder
print "Creating encoder with id=%s for: %s" % (Encoder.id(), destination)
encoder = Encoder(destination)

gain = 1
if max_level > 0:
    gain = 0.9 / max_level

effect = examples.Gain(gain)

decoder.setup()
effect.setup(decoder.channels(), decoder.samplerate())
encoder.setup(effect.channels(), effect.samplerate())

print "Applying effect id=%s with gain=%f" % (effect.id(), gain)

while True:
    frames, eod = decoder.process()
    encoder.process(*effect.process(frames, eod))
    if eod:
        break

