# -*- coding: utf-8 -*-
#
# Copyright (c) 2007-2009 Guillaume Pellerin <yomguy@parisson.com>

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

# Authors:
#   Guillaume Pellerin <yomguy at parisson.com>
#   Paul Brossier <piem@piem.org>
import numpy
numpy_data_types = [
    #'float128',
    'float64',
    'float32',
    'float16',
    'int64',
    'int16',
    'int32',
    'int8',
    'uint64',
    'uint32',
    'uint16',
    'uint8',
    #'timedelta64',
    #'datetime64',
    #'complex128',',
    #'complex64',
    ]
numpy_data_types = map(lambda x: getattr(numpy,x), numpy_data_types)
numpy_data_types += [numpy.ndarray]

class AnalyzerResult(dict):

    def __init__(self, id = "", name = "", unit = "s", value = None):
        self['id'] = id
        self['name'] = name
        self['unit'] = unit
        self['value'] = value

    def __setattr__(self, name, value):
        # make a numpy.array out of list
        if type(value) is list:
            value = numpy.array(value)
        # serialize using numpy
        if type(value) in numpy_data_types:
            value = value.tolist()
        if type(value) not in [list, str, int, long, float, complex, type(None)] + numpy_data_types:
            raise TypeError, 'AnalyzerResult can not accept type %s' % type(value)
        if name == 'value': self['value'] = value
        return super(AnalyzerResult, self).__setattr__(name, value)

    def __getattr__(self, name):
        if name in ['id', 'name', 'unit', 'value']:
            return self[name]
        return super(AnalyzerResult, self).__getattr__(name)

class AnalyzerResultContainer(object):

    def __init__(self, analyzer_results = []):
        self.results = analyzer_results

    def __getitem__(self, i):
        return self.results[i]

    def __len__(self):
        return len(self.results)

    def __repr__(self):
        return self.to_json()

    def to_xml(self, data_list = None):
        if data_list == None: data_list = self.results
        import xml.dom.minidom
        doc = xml.dom.minidom.Document()
        root = doc.createElement('telemeta')
        doc.appendChild(root)
        for data in data_list:
            node = doc.createElement('data')
            for a in ['name', 'id', 'unit', 'value']:
                node.setAttribute(a, str(data[a]) )
            if type(data['value']) != type(str()) and type(data['value']) != type(unicode()):
                node.setAttribute('str', '0')
            root.appendChild(node)
        return xml.dom.minidom.Document.toprettyxml(doc)

    def from_xml(self, xml_string):
        import xml.dom.minidom
        doc = xml.dom.minidom.parseString(xml_string)
        root = doc.getElementsByTagName('telemeta')[0]
        results = []
        for child in root.childNodes:
            if child.nodeType != child.ELEMENT_NODE: continue
            child_dict = {}
            for a in ['name', 'id', 'unit', 'value']:
                child_dict[a] = str(child.getAttribute(a))
            if child.getAttribute('str') == '0':
                try:
                    child_dict['value'] = eval(child_dict['value'])
                except Exception, e:
                    print e
            results.append(child_dict)
        return results

    def to_json(self, data_list = None):
        if data_list == None: data_list = self.results
        import simplejson as json
        data_strings = []
        for data in data_list:
            data_dict = {}
            for a in ['name', 'id', 'unit', 'value']:
                data_dict[a] = data[a]
            data_strings.append(data_dict)
        return json.dumps(data_strings)

    def from_json(self, json_str):
        import simplejson as json
        return json.loads(json_str)

    def to_yaml(self, data_list = None):
        if data_list == None: data_list = self.results
        import yaml
        data_strings = []
        for f in data_list:
            f_dict = {}
            for a in f.keys():
                f_dict[a] = f[a]
            data_strings.append(f_dict)
        return yaml.dump(data_strings, default_flow_style=False)

    def from_yaml(self, yaml_str):
        import yaml
        return yaml.load(yaml_str)

    def to_numpy(self, output_file, data_list = None):
        if data_list == None: data_list = self.results
        import numpy
        numpy.save(output_file, data_list)

    def from_numpy(self, input_file):
        import numpy
        return numpy.load(input_file)
