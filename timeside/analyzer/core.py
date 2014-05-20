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

from __future__ import division

from timeside.core import Processor
import timeside  # import __version__
import numpy
from collections import OrderedDict
import h5py
import h5tools

import os

if 'DISPLAY' not in os.environ:
    import matplotlib
    matplotlib.use('Agg')

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

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
    #'unicode_', Strings should be handled through label_metadata
    #'string_',
    'object_',
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
                    for att in self.keys())

    def keys(self):
        return [attr for attr in self._default_value.keys()]

    def values(self):
        return [self[attr] for attr in self.keys()]

    def items(self):
        return [(attr, self[attr]) for attr in self.keys()]

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
                for att in self.keys()))

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

    def to_hdf5(self, h5group):
        h5tools.dict_to_hdf5(self, h5group)

    def from_hdf5(self, h5group):
        h5tools.dict_from_hdf5(self, h5group)


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
        uuid : str
    '''
    # TODO :
    # - (long) description --> à mettre dans l'API Processor

    # Define default values
    _default_value = OrderedDict([('id', None),
                                  ('name', None),
                                  ('unit', None),
                                  ('description', None),
                                  ('date', None),
                                  ('version', None),
                                  ('author', None),
                                  ('uuid', None)])

    def __setattr__(self, name, value):
        if value is None:
            value = ''

        super(IdMetadata, self).__setattr__(name, value)


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
        is_segment : boolean
            Is the media a segment of an audio source
        sha1 : str
            Sha1 hexadecimal digest of the audio source
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
                                  ('is_segment', None),
                                  ('sha1', ''),
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

        label_type : str
            = 'mono' or 'multi'
            'mono' or 'multi' enable to specify the label mode :
            - 'mono'  : mono-label (only 1 label at a time)
            - 'multi' : multi-label (several labels can be observe
                        at the same time)


    '''

    # Define default values
    _default_value = OrderedDict([('label', {}),
                                  ('description', {}),
                                  ('label_type', 'mono')])

    def to_hdf5(self, h5group):
        """
        Save a dictionnary-like object inside a h5 file group
        """
        # Write attributes
        name = 'label_type'
        if self.__getattribute__(name) is not None:
            h5group.attrs[name] = self.__getattribute__(name)

        for name in ['label', 'description']:
            subgroup = h5group.create_group(name)
            h5tools.dict_to_hdf5(self.__getattribute__(name), subgroup)


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


class DataObject(MetadataObject):

    '''
    Metadata object to handle data related Metadata

        Attributes
        ----------
        value : numpy array
        label : numpy array of int
        time : numpy array of float
        duration : numpy array of float

    '''

    # Define default values
    _default_value = OrderedDict([('value', None),
                                  ('label', None),
                                  ('time', None),
                                  ('duration', None)])

    def __setattr__(self, name, value):
        if value is None:
            value = []

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

        super(DataObject, self).__setattr__(name, value)

    def __eq__(self, other):
        try:
            return (isinstance(other, self.__class__) and
                    all([numpy.array_equal(self[key], other[key])
                         for key in self.keys()]))
        except AttributeError:
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

    def to_hdf5(self, h5group):
        # Write Datasets
        for key in self.keys():
            if self.__getattribute__(key) is None:
                continue
            if self.__getattribute__(key).dtype == 'object':
                # Handle numpy type = object as vlen string
                h5group.create_dataset(key,
                                       data=self.__getattribute__(
                                           key).tolist().__repr__(),
                                       dtype=h5py.special_dtype(vlen=str))
            else:
                if numpy.prod(self.__getattribute__(key).shape):
                    maxshape = None
                else:
                    maxshape = (None,)
                h5group.create_dataset(
                    key, data=self.__getattribute__(key), maxshape=maxshape)

    def from_hdf5(self, h5group):
        for key, dataset in h5group.items():
            # Load value from the hdf5 dataset and store in data
            # FIXME : the following conditional statement is to prevent
            # reading an empty dataset.
            # see : https://github.com/h5py/h5py/issues/281
            # It should be fixed by the next h5py version
            if dataset.shape != (0,):
                if h5py.check_dtype(vlen=dataset.dtype):
                    # to deal with VLEN data used for list of
                    # list
                    self.__setattr__(key, eval(dataset[...].tolist()))
                else:
                    self.__setattr__(key, dataset[...])
            else:
                self.__setattr__(key, [])


class AnalyzerParameters(dict):

    def as_dict(self):
        return self

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

    def to_hdf5(self, subgroup):
        h5tools.dict_to_hdf5(self, subgroup)

    def from_hdf5(self, h5group):
        h5tools.dict_from_hdf5(self, h5group)


class AnalyzerResult(MetadataObject):

    """
    Object that contains the metadata and parameters of an analyzer process

    Parameters
    ----------
    data_mode : str
        data_mode describes the type of data :
            - 'value' for values
            - 'label' for label data see LabelMetadata
    time_mode : str
        time_mode describes the correspondance between data values and time
            - 'framewise'
            - 'global'
            - 'segment'
            - 'event'

    Returns
    -------
    A new MetadataObject with the following attributes :
        - data_object : :class:`DataObject`
        - id_metadata : :class:`IdMetadata`
        - audio_metadata : :class:`AudioMetadata`
        - frame_metadata : :class:`FrameMetadata`
        - label_metadata : :class:`LabelMetadata`
        - parameters : :class:`AnalyzerParameters` Object

    """

    # Define default values
    _default_value = OrderedDict([('id_metadata', None),
                                  ('data_object', None),
                                  ('audio_metadata', None),
                                  ('frame_metadata', None),
                                  ('label_metadata', None),
                                  ('parameters', None)
                                  ])

    def __init__(self, data_mode=None, time_mode=None):
        super(AnalyzerResult, self).__init__()

        self.id_metadata = IdMetadata()
        self.data_object = DataObject()
        self.audio_metadata = AudioMetadata()
        self.frame_metadata = FrameMetadata()
        self.label_metadata = LabelMetadata()
        self.parameters = AnalyzerParameters()

    @staticmethod
    def factory(data_mode='value', time_mode='framewise'):
        """
        Factory function for Analyzer result
        """
        for result_cls in AnalyzerResult.__subclasses__():
            if (hasattr(result_cls, '_time_mode') and
                hasattr(result_cls, '_data_mode') and
                (result_cls._data_mode, result_cls._time_mode) == (data_mode,
                                                                   time_mode)):
                return result_cls()
        print data_mode, time_mode
        raise ValueError('Wrong arguments')

    def __setattr__(self, name, value):
        if name in ['_data_mode', '_time_mode']:
            super(MetadataObject, self).__setattr__(name, value)
            return

        elif name in self.keys():
            if isinstance(value, dict) and value:
                for (sub_name, sub_value) in value.items():
                    self[name][sub_name] = sub_value
                return

        super(AnalyzerResult, self).__setattr__(name, value)

    def __len__(self):
        if self.data_mode == 'value':
            return len(self.data_object.value)
        else:
            return len(self.data_object.label)

    def as_dict(self):
        return dict([(key, self[key].as_dict())
                    for key in self.keys() if hasattr(self[key], 'as_dict')] +
                    [('data_mode', self.data_mode), ('time_mode', self.time_mode)])
                    # TODO : check if it can be simplified now

    def to_xml(self):
        import xml.etree.ElementTree as ET
        root = ET.Element('result')
        root.metadata = {'name': self.id_metadata.name,
                         'id': self.id_metadata.id}

        for name in ['data_mode', 'time_mode']:
            child = ET.SubElement(root, name)
            child.text = str(self.__getattribute__(name))
            child.tag = name
            root.append(child)

        for key in self.keys():
            child = ET.fromstring(self[key].to_xml())
            child.tag = key
            root.append(child)

        return ET.tostring(root, encoding="utf-8", method="xml")

    @staticmethod
    def from_xml(xml_string):
        import xml.etree.ElementTree as ET
        root = ET.fromstring(xml_string)

        data_mode_child = root.find('data_mode')
        time_mode_child = root.find('time_mode')
        result = AnalyzerResult.factory(data_mode=data_mode_child.text,
                                        time_mode=time_mode_child.text)
        for child in root:
            key = child.tag
            if key not in ['data_mode', 'time_mode']:
                child_string = ET.tostring(child)
                result[key].from_xml(child_string)

        return result

    def to_hdf5(self, h5_file):
        # Save results in HDF5 Dataset
        group = h5_file.create_group(self.id_metadata.id)
        group.attrs['data_mode'] = self.__getattribute__('data_mode')
        group.attrs['time_mode'] = self.__getattribute__('time_mode')
        for key in self.keys():
            if key in ['data_mode', 'time_mode']:
                continue
            subgroup = group.create_group(key)
            self.__getattribute__(key).to_hdf5(subgroup)

    @staticmethod
    def from_hdf5(h5group):
        # Read Sub-Group
        result = AnalyzerResult.factory(data_mode=h5group.attrs['data_mode'],
                                        time_mode=h5group.attrs['time_mode'])
        for subgroup_name, h5subgroup in h5group.items():
            result[subgroup_name].from_hdf5(h5subgroup)
        return result

    def _render_plot(self, ax):
        return NotImplemented

    def render(self):
        '''Render a matplotlib figure from the analyzer result

           Return the figure, use fig.show() to display if neeeded
        '''
        # TODO : this may crash if the data array is too large
        # possible workaround downsampled the data
        #  and plot center, min, max values
        # see http://stackoverflow.com/a/8881973

        fig, ax = plt.subplots()
        self._render_plot(ax)
        return fig

    def _render_PIL(self, size=(1024, 256), dpi=80):
        from ..grapher.core import Image
        image_width, image_height = size

        xSize = image_width / dpi
        ySize = image_height / dpi

        fig = Figure(figsize=(xSize, ySize), dpi=dpi)

        ax = fig.add_axes([0, 0, 1, 1], frame_on=False)

        self._render_plot(ax)

        ax.autoscale(axis='x', tight=True)

        # Export to PIL image
        from StringIO import StringIO
        imgdata = StringIO()
        canvas = FigureCanvas(fig)
        canvas.print_png(imgdata, dpi=dpi)
        imgdata.seek(0)  # rewind the data

        return Image.open(imgdata)

    @property
    def data_mode(self):
        return self._data_mode

    @property
    def time_mode(self):
        return self._time_mode

    @property
    def data(self):
        raise NotImplementedError

    @property
    def time(self):
        raise NotImplementedError

    @property
    def duration(self):
        raise NotImplementedError

    @property
    def id(self):
        return self.id_metadata.id

    @property
    def name(self):
        return self.id_metadata.name

    @property
    def unit(self):
        return self.id_metadata.unit


class ValueObject(object):
    _data_mode = 'value'

    def __init__(self):
        super(ValueObject, self).__init__()
        del self.data_object.label
        del self.label_metadata

    @property
    def data(self):
        return self.data_object.value

    @property
    def properties(self):
        return dict(mean=numpy.mean(self.data, axis=0),
                    std=numpy.std(self.data, axis=0, ddof=1),
                    median=numpy.median(self.data, axis=0),
                    max=numpy.max(self.data, axis=0),
                    min=numpy.min(self.data, axis=0),
                    shape=self.data.shape,
                    )


class LabelObject(object):
    _data_mode = 'label'

    def __init__(self):
        super(LabelObject, self).__init__()
        del self.data_object.value

    @property
    def data(self):
        return self.data_object.label


class GlobalObject(object):
    _time_mode = 'global'

    def __init__(self):
        super(GlobalObject, self).__init__()
        del self.frame_metadata
        del self.data_object.time
        del self.data_object.duration

    @property
    def time(self):
        return self.audio_metadata.start

    @property
    def duration(self):
        return self.audio_metadata.duration


class FramewiseObject(object):
    _time_mode = 'framewise'

    def __init__(self):
        super(FramewiseObject, self).__init__()
        del self.data_object.time
        del self.data_object.duration

    @property
    def time(self):
        return (self.audio_metadata.start +
                self.frame_metadata.stepsize /
                self.frame_metadata.samplerate *
                numpy.arange(0, len(self)))

    @property
    def duration(self):
        return (self.frame_metadata.blocksize / self.frame_metadata.samplerate
                * numpy.ones(len(self)))


class EventObject(object):
    _time_mode = 'event'

    def __init__(self):
        super(EventObject, self).__init__()
        del self.frame_metadata
        del self.data_object.duration

    @property
    def time(self):
        return self.audio_metadata.start + self.data_object.time

    @property
    def duration(self):
        return numpy.zeros(len(self))

    def _render_plot(self, ax):
        ax.stem(self.time, self.data)


class SegmentObject(EventObject):
    _time_mode = 'segment'

    def __init__(self):
        super(EventObject, self).__init__()
        del self.frame_metadata

    @property
    def duration(self):
        return self.data_object.duration


class GlobalValueResult(ValueObject, GlobalObject, AnalyzerResult):
    pass


class GlobalLabelResult(LabelObject, GlobalObject, AnalyzerResult):
    pass


class FrameValueResult(ValueObject, FramewiseObject, AnalyzerResult):

    def _render_plot(self, ax):
        ax.plot(self.time, self.data)


class FrameLabelResult(LabelObject, FramewiseObject, AnalyzerResult):

    def _render_plot(self, ax):
        pass


class EventValueResult(ValueObject, EventObject, AnalyzerResult):
    pass


class EventLabelResult(LabelObject, EventObject, AnalyzerResult):
    pass


class SegmentValueResult(ValueObject, SegmentObject, AnalyzerResult):

    def _render_plot(self, ax):
        for time, value in (self.time, self.data):
            ax.axvline(time, ymin=0, ymax=value, color='r')
            # TODO : check value shape !!!


class SegmentLabelResult(LabelObject, SegmentObject, AnalyzerResult):

    def _render_plot(self, ax):
        import itertools
        colors = itertools.cycle(['b', 'g', 'r', 'c', 'm', 'y', 'k'])
        ax_color = {}
        for key in self.label_metadata.label.keys():
            ax_color[key] = colors.next()
        for time, duration, label in zip(self.time, self.duration, self.data):
            ax.axvspan(time, time + duration, color=ax_color[label], alpha=0.3)


class AnalyzerResultContainer(dict):

    '''
    >>> import timeside
    >>> from timeside.analyzer.core import Analyzer
    >>> wav_file = 'tests/samples/sweep.mp3' # doctest: +SKIP
    >>> d = timeside.decoder.file.FileDecoder(wav_file)

    >>> a = Analyzer()
    >>> (d|a).run()
    >>> a.new_result() #doctest: +ELLIPSIS
    FrameValueResult(id_metadata=IdMetadata(id='analyzer', name='Generic analyzer', unit='', description='', date='...', version='...', author='TimeSide', uuid='...'), data_object=DataObject(value=array([], dtype=float64)), audio_metadata=AudioMetadata(uri='...', start=0.0, duration=8.0..., is_segment=False, sha1='...', channels=2, channelsManagement=''), frame_metadata=FrameMetadata(samplerate=44100, blocksize=8192, stepsize=8192), parameters={})
    >>> resContainer = timeside.analyzer.core.AnalyzerResultContainer()
    '''

    def __init__(self, analyzer_results=None):
        super(AnalyzerResultContainer, self).__init__()
        if analyzer_results is not None:
            self.add(analyzer_results)

    def add(self, analyzer_result):
        if isinstance(analyzer_result, list):
            for res in analyzer_result:
                self.add(res)
            return
        # Check result
        if not isinstance(analyzer_result, AnalyzerResult):
            raise TypeError('only AnalyzerResult can be added')

        self.__setitem__(analyzer_result.id_metadata.id,
                         analyzer_result)
        #self.results += [analyzer_result]

    def to_xml(self, output_file=None):

        import xml.etree.ElementTree as ET
        # TODO : cf. telemeta util
        root = ET.Element('timeside')

        for result in self.values():
            if result is not None:
                root.append(ET.fromstring(result.to_xml()))

        xml_str = ET.tostring(root, encoding="utf-8", method="xml")
        if output_file:
            open(output_file, 'w').write(xml_str)
        else:
            return xml_str

    @staticmethod
    def from_xml(xml_string):
        import xml.etree.ElementTree as ET

        results = AnalyzerResultContainer()
        # TODO : from file
        #tree = ET.parse(xml_file)
        #root = tree.getroot()
        root = ET.fromstring(xml_string)
        for child in root.iter('result'):
            results.add(AnalyzerResult.from_xml(ET.tostring(child)))

        return results

    def to_json(self, output_file=None):
        #if data_list == None: data_list = self.results
        import simplejson as json

        # Define Specialize JSON encoder for numpy array
        def NumpyArrayEncoder(obj):
            if isinstance(obj, numpy.ndarray):
                return {'numpyArray': obj.tolist(),
                        'dtype': obj.dtype.__str__()}
            elif isinstance(obj, numpy.generic):
                return numpy.asscalar(obj)
            else:
                print type(obj)
                raise TypeError(repr(obj) + " is not JSON serializable")

        json_str = json.dumps([res.as_dict() for res in self.values()],
                              default=NumpyArrayEncoder)
        if output_file:
            open(output_file, 'w').write(json_str)
        else:
            return json_str

    @staticmethod
    def from_json(json_str):
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

            res = AnalyzerResult.factory(data_mode=res_json['data_mode'],
                                         time_mode=res_json['time_mode'])
            for key in res_json.keys():
                if key not in ['data_mode', 'time_mode']:
                    res[key] = res_json[key]

            results.add(res)
        return results

    def to_yaml(self, output_file=None):
        #if data_list == None: data_list = self.results
        import yaml

        # Define Specialize Yaml encoder for numpy array
        def numpyArray_representer(dumper, obj):
            return dumper.represent_mapping(u'!numpyArray',
                                            {'dtype': obj.dtype.__str__(),
                                             'array': obj.tolist()})

        yaml.add_representer(numpy.ndarray, numpyArray_representer)

        yaml_str = yaml.dump([res.as_dict() for res in self.values()])
        if output_file:
            open(output_file, 'w').write(yaml_str)
        else:
            return yaml_str

    @staticmethod
    def from_yaml(yaml_str):
        import yaml

        # Define Specialize Yaml encoder for numpy array
        def numpyArray_constructor(loader, node):
            mapping = loader.construct_mapping(node, deep=True)
            return numpy.asarray(mapping['array'], dtype=mapping['dtype'])

        yaml.add_constructor(u'!numpyArray', numpyArray_constructor)

        results_yaml = yaml.load(yaml_str)
        results = AnalyzerResultContainer()
        for res_yaml in results_yaml:
            res = AnalyzerResult.factory(data_mode=res_yaml['data_mode'],
                                         time_mode=res_yaml['time_mode'])
            for key in res_yaml.keys():
                if key not in ['data_mode', 'time_mode']:
                    res[key] = res_yaml[key]
            results.add(res)
        return results

    def to_numpy(self, output_file=None):
        if output_file:
            numpy.save(output_file, self)
        else:
            return self

    @staticmethod
    def from_numpy(input_file):
        return numpy.load(input_file)

    def to_hdf5(self, output_file):
        # Open HDF5 file and save dataset (overwrite any existing file)
        with h5py.File(output_file, 'w') as h5_file:
            for res in self.values():
                res.to_hdf5(h5_file)

    @staticmethod
    def from_hdf5(input_file):
        import h5py
        # TODO : enable import for yaafe hdf5 format

        # Open HDF5 file for reading and get results
        h5_file = h5py.File(input_file, 'r')
        results = AnalyzerResultContainer()
        try:
            for group in h5_file.values():
                result = AnalyzerResult.from_hdf5(group)
                results.add(result)
        except TypeError:
            print('TypeError for HDF5 serialization')
        finally:
            h5_file.close()  # Close the HDF5 file

        return results


class Analyzer(Processor):

    '''
    Generic class for the analyzers
    '''

    type = 'analyzer'

    def __init__(self):
        super(Analyzer, self).__init__()

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

    @property
    def results(self):
        return AnalyzerResultContainer(
            [self.process_pipe.results[key] for key in self.process_pipe.results.keys()
             if key.split('.')[0] == self.id()])

    @staticmethod
    def id():
        return "analyzer"

    @staticmethod
    def name():
        return "Generic analyzer"

    @staticmethod
    def unit():
        return ""

    def new_result(self, data_mode='value', time_mode='framewise'):
        '''
        Create a new result

        Attributes
        ----------
        data_object : MetadataObject
        id_metadata : MetadataObject
        audio_metadata : MetadataObject
        frame_metadata : MetadataObject
        label_metadata : MetadataObject
        parameters : dict

        '''

        from datetime import datetime

        result = AnalyzerResult.factory(data_mode=data_mode,
                                        time_mode=time_mode)

        # Automatically write known metadata
        result.id_metadata.date = datetime.now().replace(
            microsecond=0).isoformat(' ')
        result.id_metadata.version = timeside.__version__
        result.id_metadata.author = 'TimeSide'
        result.id_metadata.id = self.id()
        result.id_metadata.name = self.name()
        result.id_metadata.unit = self.unit()
        result.id_metadata.uuid = self.uuid()

        result.audio_metadata.uri = self.mediainfo()['uri']
        result.audio_metadata.sha1 = self.mediainfo()['sha1']
        result.audio_metadata.start = self.mediainfo()['start']
        result.audio_metadata.duration = self.mediainfo()['duration']
        result.audio_metadata.is_segment = self.mediainfo()['is_segment']
        result.audio_metadata.channels = self.channels()

        if time_mode == 'framewise':
            result.frame_metadata.samplerate = self.result_samplerate
            result.frame_metadata.blocksize = self.result_blocksize
            result.frame_metadata.stepsize = self.result_stepsize

        return result

DOCTEST_ALIAS = {'wav_file':
                 'https://github.com/yomguy/timeside-samples/raw/master/samples/sweep.mp3'}


if __name__ == "__main__":
    import doctest
    doctest.testmod(extraglobs=DOCTEST_ALIAS)
