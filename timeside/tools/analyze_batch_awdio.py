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
import datetime
import timeside
from logger import Logger
import Queue
from threading import Thread
from cache import Cache


class Media2Analyzer(object):

    def __init__(self, media_dir, dest_dir,  log_file):
        self.root_dir = media_dir
        self.dest_dir = dest_dir
        self.threads = 1
        self.logger = Logger(log_file)
        self.counter = 0
        self.force = 0
        self.cache = TelemetaCache(self.dest_dir)

        self.media_list = self.get_media_list()
        if not os.path.exists(self.dest_dir):
            os.makedirs(self.dest_dir)
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
            dest_file = name + '.xml'
            if not os.path.exists(dest_file) or self.force:
                path_dict[media] = dest_file
        return path_dict

    def process(self):          
        for media, file in self.path_dict.iteritems():
	    self.analyzers = timeside.core.processors(timeside.api.IAnalyzer)
	    mess = 'Processing ' + media
	    self.logger.write_info(mess)
	    if not self.cache.exists(file):
		analyzers = []
		analyzers_sub = []
		decoder  = timeside.decoder.FileDecoder(media)
		pipe = decoder
		for analyzer in self.analyzers:
		    subpipe = analyzer()
		    analyzers_sub.append(subpipe)
		    pipe = pipe | subpipe
		pipe.run()
		
		for analyzer in analyzers_sub:
		    value = analyzer.result()
		    if analyzer.id() == 'duration':
			value = datetime.timedelta(0,value)
		    analyzers.append({'name':analyzer.name(),
				      'id':analyzer.id(),
				      'unit':analyzer.unit(),
				      'value':str(value)})
		
		self.cache.write_analyzer_xml(analyzers, file)		    


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print """
        Usage : python analyze_batch.py /path/to/media_dir /path/to/dest_dir

        Dependencies : timeside, python, python-numpy, python-gst0.10, gstreamer0.10-plugins-base
        See http://code.google.com/p/timeside/ for more information.
        """
    else:
        media_dir = sys.argv[-3]
        dest_dir = sys.argv[-2]
        log_file = sys.argv[-1]
        m = Media2Analyzer(media_dir, dest_dir, log_file)
        m.process()
