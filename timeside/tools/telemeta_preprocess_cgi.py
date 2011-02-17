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

# for python2.5

version = '0.5'


import os
import sys
import time
import shutil
import datetime
import timeside

# soon with python2.6
#from multiprocessing import Process

from django.core.management import setup_environ
from django.core.files.base import ContentFile
import cgi
fs = cgi.FieldStorage()


orig_media_dir = '/mnt/awdiomusic/musicbase'
project_dir = '/mnt/awdio'
log_file = project_dir + '/logs/process.log'
sys.path.append('/home/awdio/apps/telemeta-awdio')


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

    def __init__(self, root_dir, dest_dir, log_file):
	from telemeta.cache import TelemetaCache as Cache
	from telemeta.util.logger import Logger
	self.media_item_dir = 'items'
        self.root_dir = root_dir + 'items'
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
        self.collection_name = 'awdio'
        self.collection = self.set_collection(self.collection_name)
        
        self.analyzers = timeside.core.processors(timeside.api.IAnalyzer)
        self.grapher = timeside.grapher.WaveformAwdio(width=self.width, 
                                                         height=self.height, 
                                                         bg_color=self.bg_color, 
                                                         color_scheme=self.color_scheme)
        

    def set_collection(self, collection_name):
        import telemeta.models
        collections = telemeta.models.media.MediaCollection.objects.filter(code=collection_name)
        if not collections:
            c = telemeta.models.media.MediaCollection(code=collection_name)
            c.title = collection_name
            c.save()
            msg = 'added'
            self.logger.logger.info(collection_name, msg)
            collection = c
        else:
            collection = collections[0]
        return collection

    def process(self):
	import telemeta.models
	keys = fs.keys()
	if keys[0] == 'file':
	    filename = fs['file'].value
	    media_orig = orig_media_dir + os.sep + filename
	    media = self.root_dir + os.sep + filename
	    
	    if not os.path.exists(media):
		shutil.copy(media_orig, media)
		os.system('chmod 644 ' + media)
            
            name, ext = os.path.splitext(filename)
            size = str(self.width) + '_' + str(self.height)
            image_name = name + '.' + self.scheme.id + '.' + size + '.png'
            image = self.dest_dir + os.sep + image_name
            xml = name + '.xml'
            
            if not self.cache.exists(image_name) or not self.cache.exists(xml):
                mess = 'Processing ' + media
                self.logger.logger.info(mess)
	    
		print "Content-type: text/plain\n"
		print mess
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
		self.logger.logger.info(mess)
		self.grapher.render(output=image)
		
		mess = 'Frames / Pixel = ' + str(self.grapher.graph.samples_per_pixel)
		self.logger.logger.info(mess)
		
		for analyzer in analyzers_sub:
		    value = analyzer.result()
		    if analyzer.id() == 'duration':
			value = datetime.timedelta(0,value)
		    analyzers.append({'name':analyzer.name(),
			    'id':analyzer.id(),
			    'unit':analyzer.unit(),
			    'value':str(value)})
		
		self.cache.write_analyzer_xml(analyzers, xml)
		
		item = telemeta.models.media.MediaItem.objects.filter(code=name)
			    
		if not item:
		    item = telemeta.models.media.MediaItem(collection=self.collection, code=name)
		    item.title = name
		    item.file = self.media_item_dir + os.sep + filename
		    item.save()
		    msg = 'added item : ' + filename
		    self.logger.logger.info(self.collection_name, msg)

		pipe = 0
		decoder = 0
		
		print "OK"
		
		#except:
		    #pipe = 0
		    #decoder = 0
		    #mess = 'Could NOT process : ' + media
		    #self.logger.logger.error(mess)
		    #print mess
		    
	    else:
		mess = "Nothing to do with file : " + media
		self.logger.logger.info(mess)
		print "Content-type: text/plain\n"
		print mess
	
	else:
	    print "Content-type: text/plain\n"
	    print "No file given !"
	

if __name__ == '__main__':
    sys.path.append(project_dir)
    import settings
    setup_environ(settings)
    media_dir = settings.MEDIA_ROOT
    data_dir = settings.TELEMETA_DATA_CACHE_DIR
    t = TelemetaPreprocessImport(media_dir, data_dir, log_file)
    t.process()
