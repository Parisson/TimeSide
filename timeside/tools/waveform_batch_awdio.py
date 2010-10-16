#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2009-2010 Guillaume Pellerin <yomguy@parisson.com>

# This file is part of TimeSide.

# TimeSide is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# TimeSide is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with TimeSide.  If not, see <http://www.gnu.org/licenses/>.

# Author: Guillaume Pellerin <yomguy@parisson.com>

version = '0.2'

import os
import sys
import timeside
from logger import Logger

class GrapherScheme:

    def __init__(self):
        self.color = 255
        self.color_scheme = {
            'waveform': [ # Four (R,G,B) tuples for three main color channels for the spectral centroid method
                        (self.color,self.color,self.color)
#                        (0, 0, 0), (0, 0, 0), (0, 0, 0), (0,0,0)
                        ],
            'spectrogram': [
                        (0, 0, 0), (58/4,68/4,65/4), (80/2,100/2,153/2), (90,180,100), (224,224,44), (255,60,30), (255,255,255)
                        ]}

        # Width of the image
        self.width = 572

        # Height of the image
        self.height = 74

        # Background color
        self.bg_color = None

        # Force computation. By default, the class doesn't overwrite existing image files.
        self.force = True
        

class Media2Waveform:

    def __init__(self, media_dir, img_dir,  log_file):
        self.root_dir = os.path.join(os.path.dirname(__file__), media_dir)
        self.img_dir = os.path.join(os.path.dirname(__file__), img_dir)
        self.scheme = GrapherScheme()
        self.width = self.scheme.width
        self.height = self.scheme.height
        self.bg_color = self.scheme.bg_color
        self.color_scheme = self.scheme.color_scheme
        self.force = self.scheme.force
        self.logger = Logger(log_file)
        
        self.media_list = self.get_media_list()
        if not os.path.exists(self.img_dir):
            os.makedirs(self.img_dir)
        self.path_dict = self.get_path_dict()
                                   
    def get_media_list(self):
        media_list = []
        for root, dirs, files in os.walk(self.root_dir):
            if root:
                for file in files:
                    ext = file.split('.')[-1]
                    media_list.append(root+os.sep+file)
        return media_list

    def get_path_dict(self):
        path_dict = {}
        for media in self.media_list:
            filename = media.split(os.sep)[-1]
            name, ext = os.path.splitext(filename)
            path_dict[media] = self.img_dir + os.sep + name + '.png'
        return path_dict

    def process(self):
        for audio, image in self.path_dict.iteritems():
            if not os.path.exists(image) or self.force:
                mess = 'Processing ' + audio
                self.logger.write_info(mess)
                pipe = PipeWaveform()
                waveform = pipe.process(audio, self.width, self.height, self.bg_color, self.color_scheme)
                if os.path.exists(image):
                    os.remove(image)
                mess = 'Rendering ' + image
                self.logger.write_info(mess)
                waveform.render(output=image)
                mess = 'frames per pixel = ' + str(waveform.graph.samples_per_pixel)
                self.logger.write_info(mess)
                waveform.release()

class PipeWaveform:
    
    def process(self, audio, width, height, bg_color, color_scheme):
        decoder  = timeside.decoder.FileDecoder(audio)
        waveform = timeside.grapher.WaveformAwdio(width=width, height=height,
                                   bg_color=bg_color, color_scheme=color_scheme)
        (decoder | waveform).run()
        return waveform

if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print """
        Usage : python waveform_batch /path/to/media_dir /path/to/img_dir

        Dependencies : timeside, python, python-numpy, python-gst0.10, gstreamer0.10-plugins-base
        See http://code.google.com/p/timeside/ for more information.
        """
    else:
        media_dir = sys.argv[-3]
        img_dir = sys.argv[-2]
        log_file = sys.argv[-1]
        m = Media2Waveform(media_dir, img_dir, log_file)
        m.process()
