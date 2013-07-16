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

from utils import downsample_blocking

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
numpy_data_types = map(lambda x: getattr(numpy, x), numpy_data_types)
numpy_data_types += [numpy.ndarray]


class MetadataObject(object):
    """
    Object that contains a metadata structure
    stucture inspired by [1]
    [1] : http://www.saltycrane.com/blog/2012/08/python-data-object-motivated-desire-mutable-namedtuple-default-values/

    Metadata
    ----------


    Methods
    -------
    as_dict()
        Return a dictionnary representation of the MetadataObject
    """
    from collections import OrderedDict
    # Define default values as an OrderDict
    # in order to keep the order of the keys for display
    _default_value = OrderedDict()

    def __init__(self, **kwargs):
        '''
        Construct an Metadata object
        Abstract Class _default_value must be specified by

        Metadata()

        Parameters
        ----------

        Returns
        -------
        Metadata
        '''
        # Set Default values
        for key, value in self._default_value.items():
            setattr(self, key, value)

        # Set metadata passed in as arguments
        #for k, v in zip(self._default_value.keys(), args):
        #    setattr(self, k, v)
        #    print 'args'
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __setattr__(self, name, value):
        if name not in self._default_value.keys():
            raise AttributeError("%s is not a valid attribute in %s" %
            (name, self.__class__.__name__))
        super(MetadataObject, self).__setattr__(name, value)

    def as_dict(self):
        return dict((att, getattr(self, att))
        for att in self._default_value.keys())

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join('{}={}'.format(
            att, repr(getattr(self, att)))
            for att in self._default_value.keys()))

    def __str__(self):
        return self.as_dict().__str__()

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.as_dict() == other.as_dict())


class AnalyzerMetadata(MetadataObject):
    """
    Object that contains the metadata and parameters of an analyzer process

    Metadata
    ----------
    id : string
    name : string
    unit : string
    samplerate : int or float
    blocksize : int
    stepsize : int
    parameters : dict

    """

    from collections import OrderedDict
    # Define default values as an OrderDict
    # in order to keep the order of the keys for display
    _default_value = OrderedDict([('id', ''),
                                  ('name', ''),
                                  ('unit', ''),
                                  ('samplerate', None),
                                  ('blocksize', None),
                                  ('stepsize', None),
                                  ('parameters', {})
                                  ])
    # TODO : rajouter
    # - version timeside
    # - date import datetime format iso
    # - filename (audio)
    # - (long) description --> à mettre dans l'API Processor


class AnalyzerResult(object):
    """
    Object that contains results return by an analyzer process
    metadata :
        - data :
        - metadata : an AnalyzerMetadata object containing the metadata
    """
    def __init__(self, data=None, metadata=None):
        # Define Metadata
        if metadata is None:
            self.metadata = AnalyzerMetadata()
        else:
            self.metadata = metadata

        # Define Data
        if data is None:
            self.data = []
        else:
            self.data = data

    def __setattr__(self, name, value):
        # Set Data with the proper type
        if name == 'data':
            if value is None:
                value = []
            # make a numpy.array out of list
            if type(value) is list:
                value = numpy.array(value)
            # serialize using numpy
            if type(value) in numpy_data_types:
                value = value.tolist()
            if type(value) not in [list, str, int, long, float, complex, type(None)] + numpy_data_types:
                raise TypeError('AnalyzerResult can not accept type %s' %
                type(value))
        elif name == 'metadata':
            if not isinstance(value, AnalyzerMetadata):
                value = AnalyzerMetadata(**value)
        else:
            raise AttributeError("%s is not a valid attribute in %s" %
            (name, self.__class__.__name__))

        return super(AnalyzerResult, self).__setattr__(name, value)

    @property
    def properties(self):
        prop = dict(mean=numpy.mean(self.data, axis=0),
                     std=numpy.std(self.data, axis=0, ddof=1),
                     median=numpy.median(self.data, axis=0),
                     max=numpy.max(self.data, axis=0),
                     min=numpy.min(self.data, axis=0)
                     )
                     # ajouter size
        return(prop)
#    def __getattr__(self, name):
#        if name in ['id', 'name', 'unit', 'value', 'metadata']:
#            return self[name]
#        return super(AnalyzerResult, self).__getattr__(name)

    def as_dict(self):
        return(dict(data=self.data, metadata=self.metadata.as_dict()))

    def to_json(self):
        import simplejson as json
        return json.dumps(self.as_dict())

    def __repr__(self):
        return self.to_json()

    def __eq__(self,other):
        return (isinstance(other, self.__class__)
            and self.as_dict() == other.as_dict())

    def __ne__(self, other):
        return not self.__eq__(other)

class AnalyzerResultContainer(object):

    def __init__(self, analyzer_results=None):
        self.results = []
        if analyzer_results is not None:
            self.add_result(analyzer_results)

    def __getitem__(self, i):
        return self.results[i]

    def __len__(self):
        return len(self.results)

    def __repr__(self):
        return [res.as_dict() for res in self.results].__repr__()

    def __eq__(self, other):
        if hasattr(other, 'results'):
            other = other.results
        for a, b in zip(self.results, other):
            if a != b:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def add_result(self, analyzer_result):
        if type(analyzer_result) == list:
            for res in analyzer_result:
                self.add_result(res)
            return
        if type(analyzer_result) != AnalyzerResult:
            raise TypeError('only AnalyzerResult can be added')
        self.results += [analyzer_result]

    def to_xml(self, data_list=None):
        if data_list is None:
            data_list = self.results
        import xml.etree.ElementTree as ET
        # TODO : cf. telemeta util
        root = ET.Element('timeside')

        for result in data_list:
            res_node = ET.SubElement(root, 'result')
            res_node.metadata = {'name': result.metadata.name,
                               'id': result.metadata.id}
            # Serialize Data
            data_node = ET.SubElement(res_node, 'data')
            if type(result.data) in [str, unicode]:
                data_node.text = result.data
            else:
                data_node.text = repr(result.data)
            # Serialize Metadata
            metadata_node = ET.SubElement(res_node, 'metadata')
            for (name, val) in result.metadata.as_dict().items():
                # TODO reorder keys
                child = ET.SubElement(metadata_node, name)
                if name == 'parameters':
                    for (par_key, par_val) in val.items():
                        par_child = ET.SubElement(child, par_key)
                        par_child.text = repr(par_val)
                else:
                    child.text = repr(val)

        #tree = ET.ElementTree(root)
        return ET.tostring(root, encoding="utf-8", method="xml")


    def from_xml(self, xml_string):
        import xml.etree.ElementTree as ET
        import ast

        results = AnalyzerResultContainer()
        # TODO : from file
        #tree = ET.parse(xml_file)
        #root = tree.getroot()
        root = ET.fromstring(xml_string)
        for result_child in root.iter('result'):
            result = AnalyzerResult()
            # Get data
            try:
                result.data = ast.literal_eval(result_child.find('data').text)
            except:
                result.data = result_child.find('data').text

            # Get metadata
            for attr_child in result_child.find('metadata'):
                name = attr_child.tag
                if name == 'parameters':
                    parameters = dict()
                    for param_child in attr_child:
                        par_key = param_child.tag
                        par_val = param_child.text
                        parameters[par_key] = ast.literal_eval(par_val)
                    value = parameters
                else:
                    value = ast.literal_eval(attr_child.text)
                result.metadata.__setattr__(name, value)
            results.add_result(result)

        return results


    def to_json(self):
        #if data_list == None: data_list = self.results
        import simplejson as json
        return json.dumps([res.as_dict() for res in self])

    def from_json(self, json_str):
        import simplejson as json
        results_json = json.loads(json_str)
        results = AnalyzerResultContainer()
        for res_json in results_json:
            res = AnalyzerResult(data=res_json['data'],
                                 metadata=res_json['metadata'])
            results.add_result(res)
        return results

    def to_yaml(self):
        #if data_list == None: data_list = self.results
        import yaml
        return yaml.dump([res.as_dict() for res in self])

    def from_yaml(self, yaml_str):
        import yaml

        results_yaml = yaml.load(yaml_str)
        results = AnalyzerResultContainer()
        for res_yaml in results_yaml:
            res = AnalyzerResult(data=res_yaml['data'],
                                 metadata=res_yaml['metadata'])
            results.add_result(res)
        return results

    def to_numpy(self, output_file, data_list=None):
        if data_list is None:
            data_list = self.results
        import numpy
        numpy.save(output_file, data_list)

    def from_numpy(self, input_file):
        import numpy
        return numpy.load(input_file)

    def to_hdf5(self, output_file, data_list=None):
        if data_list is None:
            data_list = self.results

        import h5py

        # Open HDF5 file and save dataset
        # TODO : Check self.results format
        # as it asumes 'id', 'name', 'value' and 'units' keys
        h5_file = h5py.File(output_file, 'w')  # overwrite any existing file
        try:
            for data in data_list:
                # Save results in HDF5 Dataset
                dset = h5_file.create_dataset(data['id'], data=data['value'])
                # Save associated metadata
                dset.attrs["unit"] = data['unit']
                dset.attrs["name"] = data['name']
        except TypeError:
            pass
        finally:
            h5_file.close()  # Close the HDF5 file

    def from_hdf5(self, input_file):
        import h5py

        # Open HDF5 file for reading and get results
        h5_file = h5py.File(input_file, 'r')
        data_list = AnalyzerResultContainer()
        try:
            for name in h5_file.keys():
                dset = h5_file.get(name)  # Read Dataset
                id = name
                # Read metadata
                unit = dset.attrs['unit']
                name = dset.attrs['name']
                # Create new AnalyzerResult
                data = AnalyzerResult(id=id, name=name, unit=unit)

                # Load value from the hdf5 dataset and store in data
                # FIXME : the following conditional statement is to prevent
                # reading an empty dataset.
                # see : https://github.com/h5py/h5py/issues/281
                # It should be fixed by the next h5py version
                if dset.shape != (0,):
                    data.value = dset[...]
                else:
                    data.value = []

                # TODO : enable import from yaafe hdf5 format
                #for attr_name in dset.attrs.keys():
                #   data[attr_name] = dset.attrs[attr_name]

                data_list.add_result(data)
        except TypeError:
            print('TypeError for HDF5 serialization')
        finally:
            h5_file.close()  # Close the HDF5 file

        return data_list