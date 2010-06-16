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

import os
import sys
from timeside.tests.api import examples
from timeside.core import *
from timeside.api import *
from grapher_scheme import *
from timeside.tests.api.gstreamer import FileDecoder


class Media2Waveform(object):

    def __init__(self, media_dir, img_dir):
        self.root_dir = media_dir
        self.img_dir = img_dir
        self.scheme = GrapherScheme()
        self.width = self.scheme.width
        self.height = self.scheme.height
        self.bg_color = self.scheme.bg_color
        self.color_scheme = self.scheme.color_scheme
        self.force = self.scheme.force

        self.media_list = self.get_media_list()
        if not os.path.exists(self.img_dir):
            os.mkdir(self.img_dir)
        self.path_dict = self.get_path_dict()

    def get_media_list(self):
        media_list = []
        for root, dirs, files in os.walk(self.root_dir):
            if root:
                for file in files:
                    ext = file.split('.')[-1]
                    if ext == 'mp3' or ext == 'MP3':
                        media_list.append(root+os.sep+file)
        return media_list

    def get_path_dict(self):
        path_dict = {}
        for media in self.media_list:
            name = os.path.splitext(media)
            name = name[0].split(os.sep)[-1]
            path_dict[media] = self.img_dir + os.sep + name + '.png'
        return path_dict

    def process(self):
        for source, image in self.path_dict.iteritems():
            if not os.path.exists(image) or self.force:
                print 'Rendering ', source, ' to ', image, '...'
                audio = os.path.join(os.path.dirname(__file__), source)
                decoder  = FileDecoder(audio)
                waveform = examples.Waveform(width=self.width, height=self.height, output=image,
                                            bg_color=self.bg_color, color_scheme=self.color_scheme)
                (decoder | waveform).run()
                print 'frames per pixel = ', waveform.graph.samples_per_pixel
                waveform.render()


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print """
        Usage : python waveform_batch.py /path/to/media_dir /path/to/img_dir

        Dependencies : python, python-numpy, python-gst0.10, gstreamer0.10-plugins-base
        See http://code.google.com/p/timeside/ for more information.
        """
    else:
        media_dir = sys.argv[-2]
        img_dir = sys.argv[-1]
        m = Media2Waveform(media_dir, img_dir)
        m.process()


