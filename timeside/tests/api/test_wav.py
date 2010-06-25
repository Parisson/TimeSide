# -*- coding: utf-8 -*-

from timeside.decoder import *
from timeside.analyzer import *
from timeside.encoder import *

import os.path
source = os.path.join(os.path.dirname(__file__),  "../samples/sweep.wav")
dest = os.path.join(os.path.dirname(__file__), "../results/sweep_wav.wav")

decoder  = FileDecoder(source)
encoder  = WavEncoder(dest)

(decoder | encoder).run()

