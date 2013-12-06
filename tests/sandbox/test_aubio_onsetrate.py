# -*- coding: utf-8 -*-

import timeside

decoder  =  timeside.decoder.FileDecoder('/home/momo/music_local/Kavinsky - Nightcall EP/01 Nightcall (Feat. Lovefoxxx).mp3')
analyzer = timeside.analyzer.AubioOnsetRate()
(decoder | analyzer).run()
print analyzer.result()


