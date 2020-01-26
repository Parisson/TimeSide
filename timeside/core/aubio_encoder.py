import aubio
import numpy as np
from timeside.core import Processor, implements, interfacedoc, abstract
from timeside.core.api import IEncoder

class AubioEncoder(Processor):
    implements(IEncoder)
    abstract()

    type = 'encoder'

    def __init__(self, output, streaming=False, overwrite=False):

        super (AubioEncoder, self).__init__()

        if isinstance(output, str):
            import os.path
            if os.path.isdir(output):
                raise IOError("Encoder output must be a file, not a directory")
            elif os.path.isfile(output) and not overwrite:
                raise IOError(
                    "Encoder output %s exists, but overwrite set to False")
            self.filename = output
        else:
            self.filename = None
        self.streaming = streaming

        if not self.filename and not self.streaming:
            raise Exception('Must give an output')

        self.eod = False
        self.metadata = None
        self.num_samples = 0

        self.sink = aubio.sink(self.filename)

    @interfacedoc
    def release(self):
        self.sink.close()

    @interfacedoc
    def set_metadata(self, metadata):
        self.metadata = metadata

    @interfacedoc
    def process(self, frames, eod=False):
        self.eod = eod
        max_write = 4096
        indices = range(max_write, frames.shape[0], max_write)
        for f_slice in np.array_split(frames, indices):
            write_frames = f_slice.shape[0]
            self.sink.do_multi(f_slice.T, write_frames)
            self.num_samples += write_frames
        return frames, eod
