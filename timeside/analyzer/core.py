# -*- coding: utf-8 -*-
#
# Copyright (c) 2007-2013 Parisson SARL

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
from collections import OrderedDict

numpy_data_types = [
    #'float128',
    'float64',
    'float32',
    #'float16', Not supported by h5py for version < 2.2
    'int64',
    'int16',
    'int32',
    'int8',
    'uint64',
    'uint32',
    'uint16',
    'uint8',
    'object_',
    'string_',
    'longlong',
    #'timedelta64',
    #'datetime64',
    #'complex128',
    #'complex64',
]
numpy_data_types = map(lambda x: getattr(numpy, x), numpy_data_types)
#numpy_data_types += [numpy.ndarray]


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
        # for k, v in zip(self._default_value.keys(), args):
        #    setattr(self, k, v)
        #    print 'args'
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __setattr__(self, name, value):
        if name not in self._default_value.keys():
            raise AttributeError("%s is not a valid attribute in %s" %
                                 (name, self.__class__.__name__))
        super(MetadataObject, self).__setattr__(name, value)

    def __delattr__(self, name):
        if name in self._default_value.keys():
            new_default_value = self._default_value.copy()
            del new_default_value[name]
            super(MetadataObject, self).__setattr__('_default_value',
                                                    new_default_value)
            super(MetadataObject, self).__delattr__(name)

    def as_dict(self):
        return dict((att, getattr(self, att))
                    for att in self._default_value.keys())

    def keys(self):
        return [attr for attr in self._default_value.keys()
                if hasattr(self, attr)]

    def values(self):
        return [self[attr] for attr in self._default_value.keys()
                if hasattr(self, attr)]

    def items(self):
        return [(attr, self[attr]) for attr in self._default_value.keys()
                if hasattr(self, attr)]

    def __getitem__(self, key, default=None):
        try:
            return getattr(self, key)
        except AttributeError:
            return default

    def __setitem__(self, key, value):
        setattr(self, key, value)

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
                and all([self[key] == other[key] for key in self.keys()]))

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
        for child in root:
            key = child.tag
            if child.text:
                self[key] = ast.literal_eval(child.text)


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

    # Define default values
    _default_value = OrderedDict([('samplerate', None),
                                  ('blocksize', None),
                                  ('stepsize', None)])


class AnalyzerData(MetadataObject):

    '''
    Metadata object to handle Frame related Metadata

        Attributes
        ----------
        data : numpy array
        time : numpy array of float
        duration : numpy array of float

    '''

    # Define default values
    _default_value = OrderedDict([('value', None),
                                  ('label', []),
                                  ('time', []),
                                  ('duration', [])])

    def __setattr__(self, name, value):
        if value is not None:
            # Set Data with the proper type
            if name == 'value':
                value = numpy.asarray(value)
                if value.dtype.type not in numpy_data_types:
                    raise TypeError(
                        'Result Data can not accept type %s for %s' %
                        (value.dtype.type, name))
                if value.shape == ():
                    value.resize((1,))

            elif name == 'label':
                try:
                    value = numpy.asarray(value, dtype='int')
                except ValueError:
                    raise TypeError(
                        'Result Data can not accept type %s for %s' %
                        (value.dtype.type, name))

            elif name in ['time', 'duration']:
                try:
                    value = numpy.asfarray(value)
                except ValueError:
                    raise TypeError(
                        'Result Data can not accept type %s for %s' %
                        (value.dtype.type, name))
            elif name == 'dataType':
                return

        super(AnalyzerData, self).__setattr__(name, value)

    def __eq__(self, other):
        try:
            return (isinstance(other, self.__class__) and
                    all([numpy.array_equal(self[key], other[key])
                         for key in self.keys()]))
        except AttributeError:
            # print self
            # print [self[key] == other[key] for key in self.keys()]
            return (isinstance(other, self.__class__) and
                    all([bool(numpy.logical_and.reduce((self[key] == other[key]).ravel()))
                         for key in self.keys()]))

    def __ne__(self, other):
        return not(isinstance(other, self.__class__) or
                   any([numpy.array_equal(self[key], other[key])
                        for key in self.keys()]))

    def to_xml(self):
        import xml.etree.ElementTree as ET
        root = ET.Element('Metadata')

        for key in self.keys():
            child = ET.SubElement(root, key)
            value = getattr(self, key)
            if value not in [None, []]:
                child.text = repr(value.tolist())
                child.set('dtype', value.dtype.__str__())

        return ET.tostring(root, encoding="utf-8", method="xml")

    def from_xml(self, xml_string):
        import xml.etree.ElementTree as ET
        import ast
        root = ET.fromstring(xml_string)
        for child in root:
            key = child.tag
            if child.text:
                self[key] = numpy.asarray(ast.literal_eval(child.text),
                                          dtype=child.get('dtype'))


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

    def as_dict(self):
        return self


class AnalyzerResult(MetadataObject):

    """
    Object that contains the metadata and parameters of an analyzer process

    Parameters
    ----------
    dataMode : str
        dataMode describes the type of data :
            - 'value' for values
            - 'label' for label data see LabelMetadata
    timeMode : str
        timeMode describes the correspondance between data values and time
            - 'framewise'
            - 'global'
            - 'segment'
            - 'event'


    Returns
    -------
    A new MetadataObject with the following attributes :
        - dataMode
        - timeMode
        - data : :class:`AnalyzerData`
        - idMetadata : :class:`IdMetadata`
        - audioMetadata : :class:`AudioMetadata`
        - frameMetadata : :class:`FrameMetadata`
        - labelMetadata : :class:`LabelMetadata`
        - parameters : :class:`AnalyzerParameters` Object

    """

    # Define default values
    _default_value = OrderedDict([('dataMode', None),
                                  ('timeMode', None),
                                  ('idMetadata', None),
                                  ('data', None),
                                  ('audioMetadata', None),
                                  ('frameMetadata', None),
                                  ('labelMetadata', None),
                                  ('parameters', None)
                                  ])

    _validDataMode = ['value', 'label', None]
    _validTimeMode = ['framewise', 'global', 'segment', 'event', None]

    def __init__(self, dataMode=None,
                 timeMode=None):
        super(AnalyzerResult, self).__init__()
        self.dataMode = dataMode
        self.timeMode = timeMode

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
                super(AnalyzerResult, self).__setattr__(name, value)
                return
            elif isinstance(value, dict):
                for (sub_name, sub_value) in value.items():
                    self[name][sub_name] = sub_value
                return
            elif value is None:
                super(AnalyzerResult, self).__setattr__(name, setFunc())
                return
            else:
                raise TypeError('Wrong argument')
        elif name == 'dataMode':
            if self[name] is not None:
                raise AttributeError("The value of attribute ''timeMode'' \\\
                can not change after setup")
            if value == 'value':
                del self.labelMetadata
                del self.data.label
            elif value == 'label':
                del self.data.value
            elif value is None:
                pass
            else:
                raise ValueError('Argument ''dataMode''=%s should be in %s'
                                 % (value, self._validDataMode))
        elif name == 'timeMode':
            if self[name] is not None:
                raise AttributeError("The value of attribute ''timeMode'' \\\
                can not change after setup")

            if value == 'framewise':
                del self.data.time
                del self.data.duration
                pass
            elif value == 'global':
                del self.data.time
                del self.data.duration
                del self.frameMetadata

                pass
            elif value == 'segment':
                del self.frameMetadata
            elif value == 'event':
                del self.frameMetadata
                del self.data.duration

                pass
            elif value is None:
                pass
            else:
                raise ValueError('Argument ''timeMode''=%s should be in %s'
                                 % (value, self._validTimeMode))
        super(AnalyzerResult, self).__setattr__(name, value)

    def as_dict(self):
        return dict([(key, self[key].as_dict())
                    for key in self.keys() if hasattr(self[key], 'as_dict')] +
                    [('dataMode', self.dataMode), ('timeMode', self.timeMode)])

    def to_xml(self):
        import xml.etree.ElementTree as ET
        root = ET.Element('result')
        root.metadata = {'name': self.idMetadata.name,
                         'id': self.idMetadata.id}

        for key in self.keys():
            if key in ['dataMode', 'timeMode']:
                child = ET.SubElement(root, key)
                child.text = str(self[key])
            else:
                child = ET.fromstring(self[key].to_xml())
            child.tag = key
            root.append(child)

        return ET.tostring(root, encoding="utf-8", method="xml")

    def from_xml(self, xml_string):
        import xml.etree.ElementTree as ET
        root = ET.fromstring(xml_string)

        dataModeChild = root.find('dataMode')
        timeModeChild = root.find('timeMode')
        result = AnalyzerResult(dataMode=dataModeChild.text,
                                   timeMode=timeModeChild.text)
        for child in root:
            key = child.tag
            if key not in ['dataMode', 'timeMode']:
                child_string = ET.tostring(child)
                result[key].from_xml(child_string)

        return result



#    @property
#    def properties(self):
#        prop = dict(mean=numpy.mean(self.data, axis=0),
#                    std=numpy.std(self.data, axis=0, ddof=1),
#                    median=numpy.median(self.data, axis=0),
#                    max=numpy.max(self.data, axis=0),
#                    min=numpy.min(self.data, axis=0)
#                    )
#                     # ajouter size
#        return(prop)


class AnalyzerResultContainer(dict):

    '''
    >>> from timeside.decoder import FileDecoder
    >>> import timeside.analyzer.core as coreA
    >>> import os
    >>> ModulePath =  os.path.dirname(os.path.realpath(coreA.__file__))
    >>> wavFile = os.path.join(ModulePath , '../../tests/samples/sweep.wav')
    >>> d = FileDecoder(wavFile, start=1)

    >>> a = coreA.Analyzer()
    >>> (d|a).run() #doctest: +ELLIPSIS
    <timeside.core.ProcessPipe object at 0x...>
    >>> a.new_result() #doctest: +ELLIPSIS
    AnalyzerResult(dataMode=None, timeMode=None, idMetadata=IdMetadata(id='', name='', unit='', description='', date='...', version='...', author='TimeSide'), data=AnalyzerData(value=None, label=array([], dtype=int64), time=array([], dtype=float64), duration=array([], dtype=float64)), audioMetadata=AudioMetadata(uri='file:///.../tests/samples/sweep.wav', start=1.0, duration=7.0, channels=None, channelsManagement=''), frameMetadata=FrameMetadata(samplerate=None, blocksize=None, stepsize=None), labelMetadata=LabelMetadata(label=None, description=None, labelType='mono'), parameters={})
    >>> resContainer = coreA.AnalyzerResultContainer()

    '''

    def __init__(self, analyzer_results=None):
        super(AnalyzerResultContainer,self).__init__()
        if analyzer_results is not None:
            self.add(analyzer_results)

#    def __getitem__(self, i):
#        return self.results[i]

#    def __len__(self):
#        return len(self.results)

#    def __repr__(self):
 #       return [res.as_dict() for res in self.values()].__repr__()

    #def __eq__(self, other):
        #if hasattr(other, 'results'):
        #    other = other.results
   #     return self == other

    #def __ne__(self, other):
    #    return not self.__eq__(other)

    def add(self, analyzer_result):
        if isinstance(analyzer_result, list):
            for res in analyzer_result:
                self.add(res)
            return
        # Check result
        if not isinstance(analyzer_result, AnalyzerResult):
            raise TypeError('only AnalyzerResult can be added')

        self.__setitem__(analyzer_result.idMetadata.id,
                         analyzer_result)
        #self.results += [analyzer_result]

    def to_xml(self):

        import xml.etree.ElementTree as ET
        # TODO : cf. telemeta util
        root = ET.Element('timeside')

        for result in self.values():
            if result:
                root.append(ET.fromstring(result.to_xml()))

        return ET.tostring(root, encoding="utf-8", method="xml")

    def from_xml(self, xml_string):
        import xml.etree.ElementTree as ET

        results = AnalyzerResultContainer()
        # TODO : from file
        #tree = ET.parse(xml_file)
        #root = tree.getroot()
        root = ET.fromstring(xml_string)
        for child in root.iter('result'):
            result = AnalyzerResult()
            results.add(result.from_xml(ET.tostring(child)))

        return results

    def to_json(self):
        #if data_list == None: data_list = self.results
        import simplejson as json

        # Define Specialize JSON encoder for numpy array
        def NumpyArrayEncoder(obj):
            if isinstance(obj, numpy.ndarray):
                return {'numpyArray': obj.tolist(),
                        'dtype': obj.dtype.__str__()}
            raise TypeError(repr(obj) + " is not JSON serializable")

        return json.dumps([res.as_dict() for res in self.values()],
                          default=NumpyArrayEncoder)

    def from_json(self, json_str):
        import simplejson as json

        # Define Specialize JSON decoder for numpy array
        def NumpyArrayDecoder(obj):
            if isinstance(obj, dict) and 'numpyArray' in obj:
                numpy_obj = numpy.asarray(obj['numpyArray'],
                                          dtype=obj['dtype'])
                return numpy_obj
            else:
                return obj

        results_json = json.loads(json_str, object_hook=NumpyArrayDecoder)
        results = AnalyzerResultContainer()
        for res_json in results_json:

            res = AnalyzerResult(dataMode=res_json['dataMode'],
                                    timeMode=res_json['timeMode'])
            for key in res_json.keys():
                if key not in ['dataMode', 'timeMode']:
                    res[key] = res_json[key]

            results.add(res)
        return results

    def to_yaml(self):
        #if data_list == None: data_list = self.results
        import yaml

        # Define Specialize Yaml encoder for numpy array
        def numpyArray_representer(dumper, obj):
            return dumper.represent_mapping(u'!numpyArray',
                                            {'dtype': obj.dtype.__str__(),
                                             'array': obj.tolist()})

        yaml.add_representer(numpy.ndarray, numpyArray_representer)

        return yaml.dump([res.as_dict() for res in self.values()])

    def from_yaml(self, yaml_str):
        import yaml

        # Define Specialize Yaml encoder for numpy array
        def numpyArray_constructor(loader, node):
            mapping = loader.construct_mapping(node, deep=True)
            return numpy.asarray(mapping['array'], dtype=mapping['dtype'])

        yaml.add_constructor(u'!numpyArray', numpyArray_constructor)

        results_yaml = yaml.load(yaml_str)
        results = AnalyzerResultContainer()
        for res_yaml in results_yaml:
            res = AnalyzerResult()
            for key in res_yaml.keys():
                res[key] = res_yaml[key]
            results.add(res)
        return results

    def to_numpy(self, output_file):
        numpy.save(output_file, self)

    def from_numpy(self, input_file):
        return numpy.load(input_file)

    def to_hdf5(self, output_file):

        import h5py

        # Open HDF5 file and save dataset (overwrite any existing file)
        with h5py.File(output_file, 'w') as h5_file:
            for res in self.values():
                # Save results in HDF5 Dataset
                group = h5_file.create_group(res.idMetadata.id)
                group.attrs['dataMode'] = res['dataMode']
                group.attrs['timeMode'] = res['timeMode']
                for key in res.keys():
                    if key not in ['dataMode', 'timeMode', 'data']:
                        subgroup = group.create_group(key)

                        # Write attributes
                        attrs = res[key].keys()
                        for name in attrs:
                            if res[key][name] is not None:
                                subgroup.attrs[name] = res[key][name]

                # Write Datasets
                key = 'data'
                subgroup = group.create_group(key)
                for dsetName in res[key].keys():
                    if res[key][dsetName] is not None:
                        if res[key][dsetName].dtype == 'object':
                            # Handle numpy type = object as vlen string
                            subgroup.create_dataset(dsetName,
                                                    data=res[key][
                                                        dsetName].tolist(
                                                    ).__repr__(),
                                                    dtype=h5py.special_dtype(vlen=str))
                        else:
                            subgroup.create_dataset(dsetName,
                                                    data=res[key][dsetName])

    def from_hdf5(self, input_file):
        import h5py
        # TODO : enable import for yaafe hdf5 format

        # Open HDF5 file for reading and get results
        h5_file = h5py.File(input_file, 'r')
        data_list = AnalyzerResultContainer()
        try:
            for (group_name, group) in h5_file.items():

                result = AnalyzerResult(dataMode=group.attrs['dataMode'],
                                           timeMode=group.attrs['timeMode'])
                # Read Sub-Group
                for subgroup_name, subgroup in group.items():
                    # Read attributes
                    for name, value in subgroup.attrs.items():
                            result[subgroup_name][name] = value

                    if subgroup_name == 'data':
                        for dsetName, dset in subgroup.items():
                            # Load value from the hdf5 dataset and store in data
                            # FIXME : the following conditional statement is to prevent
                            # reading an empty dataset.
                            # see : https://github.com/h5py/h5py/issues/281
                            # It should be fixed by the next h5py version
                            if dset.shape != (0,):
                                if h5py.check_dtype(vlen=dset.dtype):
                                    # to deal with VLEN data used for list of
                                    # list
                                    result[subgroup_name][dsetName] = eval(
                                        dset[...].tolist())
                                else:
                                    result[subgroup_name][dsetName] = dset[...]
                            else:
                                result[subgroup_name][dsetName] = []

                data_list.add(result)
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

        # Set default values for result_* attributes
        # may be overwritten by the analyzer
        self.result_channels = self.input_channels
        self.result_samplerate = self.input_samplerate
        self.result_blocksize = self.input_blocksize
        self.result_stepsize = self.input_stepsize

    def results(self):
        #TODO :return self._results[id=analyzerID]
        return self._results

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

    def new_result(self, dataMode=AnalyzerResult._default_value['dataMode'],
                   timeMode=AnalyzerResult._default_value['timeMode']):
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

        result = AnalyzerResult(dataMode=dataMode, timeMode=timeMode)
        # Automatically write known metadata
        result.idMetadata = IdMetadata(
            date=datetime.now().replace(microsecond=0).isoformat(' '),
            version=TimeSideVersion,
            author='TimeSide')
        result.audioMetadata = AudioMetadata(uri=self.mediainfo()['uri'],
                                             start=self.mediainfo()['start'],
                                             duration=self.mediainfo()['duration'])

        result.data = AnalyzerData()

        if dataMode == 'value':
            pass
        elif dataMode == 'label':
            result.labelMetadata = LabelMetadata()
        else:
            # raise ArgError('')
            pass

        if timeMode == 'framewise':
            result.frameMetadata = FrameMetadata(
                samplerate=self.result_samplerate,
                blocksize=self.result_blocksize,
                stepsize=self.result_stepsize)
        elif timeMode == 'global':
            # None : handle by data
            pass
        elif timeMode == 'segment':
            # None : handle by data
            pass
        elif timeMode == 'event':
            # None : handle by data, duration = 0
            pass
        else:
            # raise ArgError('')
            pass

        return result


if __name__ == "__main__":
    import doctest
    doctest.testmod()
