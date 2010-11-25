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

version = '0.3'

import os
import sys
import time
import timeside
from logger import Logger
import Queue
from threading import Thread

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

        # Grapher id
        self.id = 'waveform_awdio'

        # Width of the image
        self.width = 1800

        # Height of the image
        self.height = 233

        # Background color
        self.bg_color = None

        # Force computation. By default, the class doesn't overwrite existing image files.
        self.force = False
        
        # Nb of threads
        # FIXME: memory leak for > 1 !
        self.threads = 1


class Media2Waveform(object):

    def __init__(self, media_dir, img_dir,  log_file):
        self.root_dir = os.path.join(os.path.dirname(__file__), media_dir)
        self.img_dir = os.path.join(os.path.dirname(__file__), img_dir)
        self.scheme = GrapherScheme()
        self.width = self.scheme.width
        self.height = self.scheme.height
        self.bg_color = self.scheme.bg_color
        self.color_scheme = self.scheme.color_scheme
        self.force = self.scheme.force
        self.threads = self.scheme.threads
        self.logger = Logger(log_file)
        self.counter = 0

        self.media_list = self.get_media_list()
        if not os.path.exists(self.img_dir):
            os.makedirs(self.img_dir)
        self.path_dict = self.get_path_dict()
                                   
    def get_media_list(self):
        media_list = []
        for root, dirs, files in os.walk(self.root_dir):
            if root:
                for file in files:
                    if file[0] != '.':
                        ext = file.split('.')[-1]
                        media_list.append(root+os.sep+file)
        return media_list

    def get_path_dict(self):
        path_dict = {}
        for media in self.media_list:
            filename = media.split(os.sep)[-1]
            name, ext = os.path.splitext(filename)
            size = str(self.width) + '_' + str(self.height)
            image = self.img_dir + os.sep + name + '.' + self.scheme.id + '.' + size + '.png'
            if not os.path.exists(image) or self.force:
                path_dict[media] = image
        return path_dict

    def process(self):
        q = Queue.Queue()
        for i in range(0, self.threads):
            worker = Thread(target=Worker, args=(self.width, self.height, self.bg_color, self.color_scheme, q, self.logger))
            worker.setDaemon(True)
            worker.start()
        
        mess = str(self.threads) + ' thread(s) started'
        self.logger.write_info(mess)
            
        for media, image in self.path_dict.iteritems():
            q.put((media, image))
        q.join()
            
        
def Worker(width, height, bg_color, color_scheme, q, logger):
    while True:
        media, image = q.get()
        mess = 'Processing ' + media
        logger.write_info(mess)
        decoder  = timeside.decoder.FileDecoder(media)
        grapher = timeside.grapher.WaveformAwdio(width=width, height=height, bg_color=bg_color, color_scheme=color_scheme)
        (decoder | grapher).run()
        mess = 'Rendering ' + image
        logger.write_info(mess)
        grapher.render(output=image)
        mess = 'Frames / Pixel = ' + str(grapher.graph.samples_per_pixel)
        logger.write_info(mess)
        grapher.release()
        q.task_done()
      
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
