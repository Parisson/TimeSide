# -*- coding: utf-8 -*-

class GrapherScheme:

    def __init__(self):

        self.color_scheme = {
            'waveform': [
                        (50,0,200), (0,220,80), (255,224,0), (255,0,0)
                        ],
            'spectrogram': [
                        (0, 0, 0), (58/4,68/4,65/4), (80/2,100/2,153/2), (90,180,100), (224,224,44), (255,60,30), (255,255,255)
                           ]}

        self.width = 512
        self.height = 128
        self.bg_color = (255,255,255)
        self.force = True

