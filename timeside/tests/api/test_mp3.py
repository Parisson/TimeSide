# -*- coding: utf-8 -*-

from timeside.decoder import *
from timeside.encoder import *

source = "../samples/sweep.wav"
dest = "../results/sweep_wav.mp3"

decoder  = FileDecoder(source)
encoder  = Mp3Encoder(dest)

(decoder | encoder).run()
