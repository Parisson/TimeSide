import numpy


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
