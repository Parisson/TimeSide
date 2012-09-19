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

version = '0.4'

import os
import sys
import time
import datetime
import timeside
from logger import Logger
import Queue
from threading import Thread
from cache import Cache
from django.core.management import setup_environ
from django.core.files.base import ContentFile


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
        
        
class TelemetaPreprocessImport(object):

    def __init__(self, media_dir, dest_dir,  log_file):
        self.root_dir = media_dir
        self.dest_dir = dest_dir
        self.threads = 1
        self.logger = Logger(log_file)
        self.counter = 0
        self.force = 0
        self.cache = Cache(self.dest_dir)

        self.scheme = GrapherScheme()
        self.width = self.scheme.width
        self.height = self.scheme.height
        self.bg_color = self.scheme.bg_color
        self.color_scheme = self.scheme.color_scheme
        self.force = self.scheme.force
        self.threads = self.scheme.threads
        self.logger = Logger(log_file)
        self.counter = 0        
        
        self.analyzers = timeside.core.processors(timeside.api.IAnalyzer)
        self.grapher = timeside.grapher.WaveformAwdio(width=self.width, 
                                                         height=self.height, 
                                                         bg_color=self.bg_color, 
                                                         color_scheme=self.color_scheme)
        
        self.media_list = self.get_media_list()
        if not os.path.exists(self.dest_dir):
            os.makedirs(self.dest_dir)
                                   
    def get_media_list(self):
        media_list = []
        for root, dirs, files in os.walk(self.root_dir):
            if root:
                for file in files:
                    if file[0] != '.':
                        ext = file.split('.')[-1]
                        media_list.append(root+os.sep+file)
        return media_list

    def process(self):          
        for media in self.media_list:
            filename = media.split(os.sep)[-1]
            name, ext = os.path.splitext(filename)
            size = str(self.width) + '_' + str(self.height)
            image = self.dest_dir + os.sep + name + '.' + self.scheme.id + '.' + size + '.png'
            xml = name + '.xml'
            
            if not self.cache.exists(image) or not self.cache.exists(xml):
                mess = 'Processing ' + media
                self.logger.write_info(mess)
                decoder  = timeside.decoder.FileDecoder(media)
                pipe = decoder | self.grapher
                analyzers = []
                analyzers_sub = []
                for analyzer in self.analyzers:
                    subpipe = analyzer()
                    analyzers_sub.append(subpipe)
                    pipe = pipe | subpipe
                pipe.run()
                
                mess = 'Rendering ' + image
                self.logger.write_info(mess)
                self.grapher.render(output=image)
                
                mess = 'Frames / Pixel = ' + str(self.grapher.graph.samples_per_pixel)
                self.logger.write_info(mess)
                
                for analyzer in analyzers_sub:
                    value = analyzer.result()
                    if analyzer.id() == 'duration':
                        value = datetime.timedelta(0,value)
                    analyzers.append({'name':analyzer.name(),
                              'id':analyzer.id(),
                              'unit':analyzer.unit(),
                              'value':str(value)})
                
                self.cache.write_analyzer_xml(analyzers, xml)		    

            filename = name
            data = name.split('.')
            date = data[0]
            collection_name = data[1]
            other = ''
            if len(data) > 2:
                other = '.'.join(data[2:])
                
            item = telemeta.models.media.MediaItem.objects.filter(code=filename)
            collections = telemeta.models.media.MediaCollection.objects.filter(code=collection_name)
            
            if not collections:
                c = telemeta.models.media.MediaCollection(code=collection_name)
                c.title = collection_name
                c.save()
                msg = 'added'
                self.logger.write_info(collection_name, msg)
                collection = c
            else:
                collection = collections[0]
                
            if not item:
                item = telemeta.models.media.MediaItem(collection=collection, code=filename)
                item.title = filename
                item.file = self.media_dir + os.sep + media
                item.save()
                msg = 'added item : ' + filename
                self.logger.write_info(collection_name, msg)



if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print """
        Usage : python telemeta_preprocess_batch.py /path/to/project /path/to/media_dir /path/to/dest_dir /path/to/log

        Dependencies : timeside, python, python-numpy, python-gst0.10, gstreamer0.10-plugins-base
        See http://code.google.com/p/timeside/ for more information.
        """
    else:        
        project_dir = sys.argv[-2]
        log_file = sys.argv[-1]
        sys.path.append(project_dir)
        import settings
        setup_environ(settings)
        media_dir = settings.MEDIA_ROOT
        data_dir = settings.TELEMETA_DATA_CACHE_DIR
        print media_dir,  data_dir
        t = TelemetaPreprocessImport(media_dir, data_dir, log_file)
        t.process()
