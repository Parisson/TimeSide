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
#   Thomas Fillon <thomas  at parisson.com>

from utils import downsample_blocking
from timeside.core import Processor, implements, interfacedoc
from timeside.api import IAnalyzer
from timeside import __version__ as TimeSideVersion
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

    def keys(self):
        return self.as_dict().keys()

    def values(self):
        return self.as_dict().values()

    def items(self):
        return self.as_dict().items()

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

    def __ne__(self, other):
        return not(isinstance(other, self.__class__)
            or self.as_dict() != other.as_dict())

    def to_xml(self):
        import xml.etree.ElementTree as ET
        root = ET.Element('Metadata')

        for key in self.keys():
            child = ET.SubElement(root, key)
            child.text = repr(getattr(self, key))

        return ET.tostring(root, encoding="utf-8", method="xml")

    def from_xml(self, xml_string):
        import xml.etree.ElementTree as ET
        import ast
        root = ET.fromstring(xml_string)
        for key in self.keys():
            child = root.find(key)
            if child.text:
                self.__setattr__(key, ast.literal_eval(child.text))


class IdMetadata(MetadataObject):
    '''
    Metadata object to handle Audio related Metadata

        Attributes
        ----------
        id : str
        name : str
        unit : str
        description : str
        date : str
            date and time in ISO  8601 format YYYY-MM-DDTHH:MM:SS
        version : str
        author : str
    '''
    # TODO :
    # - (long) description --> à mettre dans l'API Processor

    from collections import OrderedDict
    # Define default values
    _default_value = OrderedDict([('id', ''),
                                  ('name', ''),
                                  ('unit', ''),
                                  ('description', ''),
                                  ('date', ''),
                                  ('version', ''),
                                  ('author', '')])


class AudioMetadata(MetadataObject):
    '''
    Metadata object to handle Identification Metadata

        Attributes
        ----------
        uri : str
        start : float
            Start time of the segment in seconds
        duration : float
            Duration of the segment in seconds
        channels : int
            Number of channels
        channelsManagement : str
            A string that indicates how the channels are manage
            Examples :
                channelsManagement = '(L+R)/2'
                channelsManagement = 'R' keep only right channel
                channelsManagement = 'L' keep only left channel
                channelsManagement = 'stereo' keep both stereo channels
    '''
    from collections import OrderedDict
    # Define default values
    _default_value = OrderedDict([('uri', ''),
                                  ('start', 0),
                                  ('duration', None),
                                  ('channels', None),
                                  ('channelsManagement', '')])


class LabelMetadata(MetadataObject):
    '''
    Metadata object to handle Label Metadata

        Attributes
        ----------
        label : dict
            A dictionnary that contains :
                - label id has keys and
                - label names has values

        description : dict
            A dictionnary that contains :
                - label id has keys and
                - label descriptions has values

        labelType : str
            = 'mono' or 'multi'
            'mono' or 'multi' enable to specify the label mode :
            - 'mono'  : mono-label (only 1 label at a time)
            - 'multi' : multi-label (several labels can be observe
                        at the same time)


    '''

    from collections import OrderedDict
    # Define default values
    _default_value = OrderedDict([('label', None),
                                  ('description', None),
                                  ('labelType', 'mono')])


class FrameMetadata(MetadataObject):
    '''
    Metadata object to handle Frame related Metadata

        Attributes
        ----------
        samplerate : int (or float?)
        blocksize : int
        stepsize : int
    '''
    # TODO : check is samplerate can support float

    from collections import OrderedDict
    # Define default values
    _default_value = OrderedDict([('samplerate', None),
                                  ('blocksize', None),
                                  ('stepsize', None)])


class AnalyzerData(MetadataObject):
    '''
    Metadata object to handle Frame related Metadata

        Attributes
        ----------
        data : numpy array or list ?
        dataType : type
        dataMode : str
            dataMode describe the type of the data :
                - 'value' for values
                - 'label' for label data
    '''
    from collections import OrderedDict
    # Define default values
    _default_value = OrderedDict([('data', None),
                                  ('dataType', ''),
                                  ('dataMode', '')])

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

            # TODO : guess dataType from value and set datType with:
            #super(AnalyzerData, self).__setattr__('dataType', dataType)

        super(AnalyzerData, self).__setattr__(name, value)


class AnalyzerParameters(dict):

    def to_xml(self):
        import xml.etree.ElementTree as ET
        root = ET.Element('Metadata')

        for key, value in self.items():
            child = ET.SubElement(root, key)
            child.text = repr(self.get(key))

        return ET.tostring(root, encoding="utf-8", method="xml")

    def from_xml(self, xml_string):
        import xml.etree.ElementTree as ET
        import ast
        root = ET.fromstring(xml_string)
        for child in root.iter():
            if child.text:
                self.set(child.tag, ast.literal_eval(child.text))


class newAnalyzerResult(MetadataObject):
    """
    Object that contains the metadata and parameters of an analyzer process

    Attributes
    ----------
    data : MetadataObject
    idMetadata : MetadataObject
    audioMetadata : MetadataObject
    frameMetadata : MetadataObject
    labelMetadata : MetadataObject
    parameters : dict

    """

    from collections import OrderedDict
    # Define default values as an OrderDict
    # in order to keep the order of the keys for display
    _default_value = OrderedDict([('idMetadata', None),
                                  ('data', None),
                                  ('audioMetadata', None),
                                  ('frameMetadata', None),
                                  ('labelMetadata', None),
                                  ('parameters', None)
                                  ])

    def __setattr__(self, name, value):
        setFuncDict = {'idMetadata': IdMetadata,
                       'data': AnalyzerData,
                       'audioMetadata': AudioMetadata,
                       'frameMetadata': FrameMetadata,
                       'labelMetadata': LabelMetadata,
                       'parameters': AnalyzerParameters}

        if name in setFuncDict.keys():
            setFunc = setFuncDict[name]
            if isinstance(value, setFunc):
                super(newAnalyzerResult, self).__setattr__(name, value)
            elif isinstance(value, dict):
                super(newAnalyzerResult, self).__setattr__(name, setFunc(**value))
            elif value in [[], None, '']:
                super(newAnalyzerResult, self).__setattr__(name, setFunc())
            else:
                raise TypeError('Wrong argument')
        elif name == 'parameters':
            if value:
                super(newAnalyzerResult, self).__setattr__(name, value)
            else:
                super(newAnalyzerResult, self).__setattr__(name, {})

    def as_dict(self):

        def makeDict(val):
            if isinstance(val, MetadataObject):
                return val.as_dict()
            elif isinstance(val, dict) or val in [None, []]:
                return val
            else:
                print val
                raise TypeError('Argument must be a dict or a MetadataObject')

        return dict((att, makeDict(getattr(self, att)))
        for att in self._default_value.keys())

    def to_xml(self):
        import xml.etree.ElementTree as ET
        root = ET.Element('result')
        root.metadata = {'name': self.idMetadata.name,
                             'id': self.idMetadata.id}

        for key in self._default_value:
            child = ET.fromstring(getattr(self, key).to_xml())
            child.tag = key
            root.append(child)

        return ET.tostring(root, encoding="utf-8", method="xml")

    def from_xml(self, xml_string):
        import xml.etree.ElementTree as ET
        root = ET.fromstring(xml_string)

        result = newAnalyzerResult()
        for key in result.keys():
            child = root.find(key)
            child_string = ET.tostring(child)
            result.__getattribute__(key).from_xml(child_string)

        return result


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

    def __eq__(self, other):
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

        return self.results == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def add_result(self, analyzer_result):
        if type(analyzer_result) == list:
            for res in analyzer_result:
                self.add_result(res)
            return
        if not (isinstance(analyzer_result, AnalyzerResult)
                or isinstance(analyzer_result, newAnalyzerResult)):
            raise TypeError('only AnalyzerResult can be added')
        self.results += [analyzer_result]

    def to_xml(self, data_list=None):
        if data_list is None:
            data_list = self.results
        import xml.etree.ElementTree as ET
        # TODO : cf. telemeta util
        root = ET.Element('timeside')

        for result in data_list:
            if result:
                root.append(ET.fromstring(result.to_xml()))

        return ET.tostring(root, encoding="utf-8", method="xml")

    def from_xml(self, xml_string):
        import xml.etree.ElementTree as ET
        import ast

        results = AnalyzerResultContainer()
        # TODO : from file
        #tree = ET.parse(xml_file)
        #root = tree.getroot()
        root = ET.fromstring(xml_string)
        for child in root.iter('result'):
            result = newAnalyzerResult()
            results.add_result(result.from_xml(ET.tostring(child)))

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
            res = newAnalyzerResult()
            res.idMetadata = res_json['idMetadata']
            res.data = res_json['data']
            res.audioMetadata = res_json['audioMetadata']
            res.frameMetadata = res_json['frameMetadata']
            res.labelMetadata = res_json['labelMetadata']
            res.parameters = res_json['parameters']

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
            res = newAnalyzerResult()
            for key in res.keys():
                res.__setattr__(key, res_yaml[key])
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
        h5_file = h5py.File(output_file, 'w')  # overwrite any existing file
        try:
            for res in data_list:
                # Save results in HDF5 Dataset
                group = h5_file.create_group(res.idMetadata.id)
                for key in res.keys():
                    if key == 'data':
                        dset = group.create_dataset(key,
                                                      data=res.data.data)
                        # Save associated metadata
                        attrs = res.data.keys()
                        attrs.remove('data')
                        for name in attrs:
                            dset.attrs[name] = res.data.__getattribute__(name)
                    else:
                        subgroup = group.create_group(key)
                        attrs = res.__getattribute__(key).keys()
                        for name in attrs:
                            value = res.__getattribute__(key).__getattribute__(name)
                            if value:
                                subgroup.attrs[name] = res.__getattribute__(key).__getattribute__(name)
                #dset.attrs["name"] = data['name']
        except TypeError:
            raise
        finally:
            h5_file.close()  # Close the HDF5 file

    def from_hdf5(self, input_file):
        import h5py
        # TODO : enable import for yaafe hdf5 format

        # Open HDF5 file for reading and get results
        h5_file = h5py.File(input_file, 'r')
        data_list = AnalyzerResultContainer()
        try:
            for (group_name, group) in h5_file.items():
                result = newAnalyzerResult()
                # Read Sub-Group
                for subgroup_name, subgroup in group.items():
                    if subgroup_name == 'data':
                        dset = subgroup
                        # Load value from the hdf5 dataset and store in data
                        # FIXME : the following conditional statement is to prevent
                        # reading an empty dataset.
                        # see : https://github.com/h5py/h5py/issues/281
                        # It should be fixed by the next h5py version
                        if dset.shape != (0,):
                            result.data.data = dset[...]
                        else:
                            result.data.data = []
                        # Load Audio metadata
                        for name, value in dset.attrs.items():
                            result.data.__setattr__(name, value)
                    else:
                        # Load Audio metadata
                        for name, value in subgroup.attrs.items():
                            result.__getattribute__(subgroup_name).__setattr__(name, value)

                data_list.add_result(result)
        except TypeError:
            print('TypeError for HDF5 serialization')
        finally:
            h5_file.close()  # Close the HDF5 file

        return data_list


class Analyzer(Processor):
    '''
    Generic class for the analyzers
    '''

    implements(IAnalyzer)

    @interfacedoc
    def setup(self, channels=None, samplerate=None,
              blocksize=None, totalframes=None):
        super(Analyzer, self).setup(channels, samplerate,
                                    blocksize, totalframes)

        # Set default values for output_* attributes
        # may be overwritten by the analyzer
        self.output_channels = self.input_channels
        self.output_samplerate = self.input_samplerate
        self.output_blocksize = self.input_blocksize
        self.output_stepsize = self.input_blocksize

    def results(self):
        container = AnalyzerResultContainer()
        return container

    @staticmethod
    @interfacedoc
    def id():
        return "analyzer"

    @staticmethod
    @interfacedoc
    def name():
        return "Generic analyzer"

    @staticmethod
    @interfacedoc
    def unit():
        return ""

    def new_result(self, dataMode='value', resultType='framewise'):
        '''
        Create a new result

        Attributes
        ----------
        data : MetadataObject
        idMetadata : MetadataObject
        audioMetadata : MetadataObject
        frameMetadata : MetadataObject
        labelMetadata : MetadataObject
        parameters : dict

        '''

        from datetime import datetime

        result = newAnalyzerResult()
        # Automatically write known metadata
        result.idMetadata = IdMetadata(date=datetime.now().replace(microsecond=0).isoformat(' '),
                                       version=TimeSideVersion,
                                       author='TimeSide')
        result.audioMetadata = AudioMetadata(uri=self.mediainfo()['uri'])

        result.data = AnalyzerData(dataMode=dataMode)

        if dataMode == 'value':
            pass
        elif dataMode == 'label':
            result.labelMetadata = LabelMetadata()
        else:
            # raise ArgError('')
            pass

        if resultType == 'framewise':
            result.frameMetadata = FrameMetadata(
                                        samplerate=self.output_samplerate,
                                        blocksize=self.output_blocksize,
                                        stepsize=self.input_stepsize)
        elif resultType == 'value':
            # None : handle by data
            pass
        elif resultType == 'segment':
            # None : handle by data
            pass
        elif resultType == 'event':
            # None : handle by data, duration = 0
            pass
        else:
            # raise ArgError('')
            pass

        return result