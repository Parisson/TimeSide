# -*- coding: utf-8 -*-

from timeside.decoder import *
from timeside.encoder import *
import os.path

source = os.path.join(os.path.dirname(__file__), "../samples/sweep.wav")
dest = os.path.join(os.path.dirname(__file__), "../results/sweep_wav.flac")

decoder  = FileDecoder(source)
encoder  = FlacEncoder(dest)

(decoder | encoder).run()
