#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2010 Guillaume Pellerin

# <yomguy@parisson.com>

# This software is a computer program whose purpose is to stream audio
# and video data through icecast2 servers.

# This software is governed by the CeCILL license under French law and
# abiding by the rules of distribution of free software. You can use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".

# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty and the software's author, the holder of the
# economic rights, and the successive licensors have only limited
# liability.

# In this respect, the user's attention is drawn to the risks associated
# with loading, using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean that it is complicated to manipulate, and that also
# therefore means that it is reserved for developers and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and, more generally, to use and operate it in the
# same conditions as regards security.

# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

# Author: Guillaume Pellerin <yomguy@parisson.com>

import os
import xml.dom.minidom


class Cache(object):

    def __init__(self, dir, params=None):
        self.dir = dir
        self.params = params
        self.files = self.get_files()

    def get_files(self):
        list = []
        for root, dirs, files in os.walk(self.dir):
            for file in files:
                list.append(file)
        return list

    def exists(self, file):
        self.files = self.get_files()
        return file in self.files

    def write_bin(self, data, file):
        path = self.dir + os.sep + file
        f = open(path, 'w')
        f.write(data)
        f.close()

    def read_bin(self, file):
        path = self.dir + os.sep + file
        f = open(path, 'r')
        data = f.read()
        f.close()
        return data

    def read_stream_bin(self, file):
        path = self.dir + os.sep + file
        chunk_size = 0x1000
        f = open(path, 'r')
        while True:
            _chunk = f.read(chunk_size)
            if not len(_chunk):
                break
            yield _chunk
        f.close()

    def write_stream_bin(self, chunk, file_object):
        file_object.write(chunk)

    def read_analyzer_xml(self, file):
        list = []
        path = self.dir + os.sep + file
        doc = xml.dom.minidom.parse(path)
        for data in doc.documentElement.getElementsByTagName('data'):
            name = data.getAttribute('name')
            id = data.getAttribute('id')
            unit = data.getAttribute('unit')
            value = data.getAttribute('value')
            list.append({'name': name, 'id': id, 'unit': unit, 'value': value})
        return list

    def write_analyzer_xml(self, data_list, file):
        path = self.dir + os.sep + file
        doc = xml.dom.minidom.Document()
        root = doc.createElement('telemeta')
        doc.appendChild(root)
        for data in data_list:
            name = data['name']
            id = data['id']
            unit = data['unit']
            value = data['value']
            node = doc.createElement('data')
            node.setAttribute('name', name)
            node.setAttribute('id', id)
            node.setAttribute('unit', unit)
            node.setAttribute('value', str(value))
            root.appendChild(node)
        f = open(path, "w")
        f.write(xml.dom.minidom.Document.toprettyxml(doc))
        f.close()
