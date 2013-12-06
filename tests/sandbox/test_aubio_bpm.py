# -*- coding: utf-8 -*-

import sys
sys.path.append('/home/momo/dev/aubio/interfaces/python/build/lib.linux-x86_64-2.6/')

import timeside

decoder  =  timeside.decoder.FileDecoder('/home/momo/music_local/Kavinsky - Nightcall EP/01 Nightcall (Feat. Lovefoxxx).mp3')
analyzer = timeside.analyzer.AubioBPM()
(decoder | analyzer).run()
print analyzer.result()


