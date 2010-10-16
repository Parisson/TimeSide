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

version = '0.1-beta'

import os
import sys
import timeside

class GrapherScheme:

    def __init__(self):

        self.color_scheme = {
            'waveform': [ # Four (R,G,B) tuples for three main color channels for the spectral centroid method
                        (50,0,200), (0,220,80), (255,224,0), (255,0,0)
                        ],
            'spectrogram': [
                        (0, 0, 0), (58/4,68/4,65/4), (80/2,100/2,153/2), (90,180,100), (224,224,44), (255,60,30), (255,255,255)
                        ]}

        # Width of the image
        self.width = 655

        # Height of the image
        self.height = 96

        # Background color
        self.bg_color = (0,0,0)

        # Force computation. By default, the class doesn't overwrite existing image files.
        self.force = True


class Media2Waveform(object):

    def __init__(self, media_dir, img_dir):
        self.root_dir = os.path.join(os.path.dirname(__file__), media_dir)
        self.img_dir = os.path.join(os.path.dirname(__file__), img_dir)
        self.scheme = GrapherScheme()
        self.width = self.scheme.width
        self.height = self.scheme.height
        self.bg_color = self.scheme.bg_color
        self.color_scheme = self.scheme.color_scheme
        self.force = self.scheme.force

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
            path_dict[media] = self.img_dir + os.sep + filename.replace('.',  '_') + '.png'
        return path_dict

    def process(self):
        for source, image in self.path_dict.iteritems():
            if not os.path.exists(image) or self.force:
                print 'Processing ', source
                audio = os.path.join(os.path.dirname(__file__), source)
                decoder  = timeside.decoder.FileDecoder(audio)
                analyzer = timeside.analyzer.Duration()
                waveform = timeside.grapher.WaveformJoyDiv(width=self.width, height=self.height,
                                            bg_color=self.bg_color, color_scheme=self.color_scheme)
                (decoder | analyzer | waveform).run()
                duration = analyzer.result()
                img_name = os.path.split(image)[1]
                image = os.path.split(image)[0]+os.sep+os.path.splitext(img_name)[0] + '_' +\
                        '_'.join([str(self.width),  str(self.height),  str(int(duration))])+os.path.splitext(img_name)[1]
                waveform.graph.filename = image
                print 'Rendering ', source, ' to ', waveform.graph.filename, '...'
                print 'frames per pixel = ', waveform.graph.samples_per_pixel
                waveform.render(output=image)
                

if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print """
        Usage : python waveform_batch /path/to/media_dir /path/to/img_dir

        Dependencies : timeside, python, python-numpy, python-gst0.10, gstreamer0.10-plugins-base
        See http://code.google.com/p/timeside/ for more information.
        """
    else:
        media_dir = sys.argv[-2]
        img_dir = sys.argv[-1]
        m = Media2Waveform(media_dir, img_dir)
        m.process()
