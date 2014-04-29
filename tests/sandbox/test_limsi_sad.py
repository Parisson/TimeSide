# -*- coding: utf-8 -*-

import timeside

decoder  =  timeside.decoder.FileDecoder('/home/momo/music_local/test/sweep.wav')
analyzer = timeside.analyzer.LimsiSad('etape')
(decoder | analyzer).run()
print analyzer.results()
