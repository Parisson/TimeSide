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

class AnalyzerResult(object):

    def __init__(self, id = "", name = "", unit = "s", value = None):
        self.id = id
        self.name = name
        self.unit = unit
        self.value = value

    def __repr__(self):
        o = {}
        for attr in ['id', 'name', 'unit', 'value']:
            o[attr] = getattr(self, attr)
        return repr(o)

    def __getitem__(self, attr):
        return getattr(self, attr)

    def __eq__(self, that):
        for attr in ['id', 'name', 'unit', 'value']:
            if getattr(self, attr) != that[attr]:
                return False
        return True

def data_to_xml(data_list):
    import xml.dom.minidom
    doc = xml.dom.minidom.Document()
    root = doc.createElement('telemeta')
    doc.appendChild(root)
    for data in data_list:
        node = doc.createElement('data')
        node.setAttribute('name', data.name)
        node.setAttribute('id', data.id)
        node.setAttribute('unit', data.unit)
        node.setAttribute('value', str(data.value))
        if type(data.value) != type(str()) and type(data.value) != type(unicode()):
            node.setAttribute('str', '0')
        root.appendChild(node)
    return xml.dom.minidom.Document.toprettyxml(doc)

def data_from_xml(xml_string):
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

def data_to_json(data_list):
    import simplejson as json
    data_strings = []
    for data in data_list:
        data_dict = {}
        for a in ['name', 'id', 'unit', 'value']:
            data_dict[a] = getattr(data,a)
        data_strings.append(data_dict)
    return json.dumps(data_strings)

def data_from_json(json_str):
    import simplejson as json
    return json.loads(json_str)

def data_to_yaml(data_list):
    import yaml
    data_strings = []
    for f in data_list:
        f_dict = {}
        for a in ['name', 'id', 'unit', 'value']:
            f_dict[a] = getattr(f,a)
        data_strings.append(f_dict)
    return yaml.dump(data_strings, default_flow_style=False)

def data_from_yaml(yaml_str):
    import yaml
    return yaml.load(yaml_str)

def data_to_numpy(data_list, output_file = None):
    import numpy
    numpy.save(output_file, data_list)

def data_from_numpy(input_file):
    import numpy
    return numpy.load(input_file)
