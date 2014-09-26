.. This file is part of TimeSide
   @author: Thomas Fillon

==========================
 Analyzer Result examples
==========================

Example of use of the Analyzer Result structure

Usage : AnalyzerResult(data_mode=None, time_mode=None)

Four different *time_mode* can be specified :

- 'framewise' : Data are returned on a frame basis (i.e. with specified blocksize, stepsize and framerate)
- 'global' : A global data value is return for the entire audio item
- 'segment' : Data are returned on a segmnet basis (i.e. with specified start time and duration)
- 'event' :  Data are returned on a segment basis (i.e. with specified start time)

Two different *data_mode* can be specified :

- 'value' : Data are returned as numpy Array of arbitrary type
- 'label' : Data are returned as label indexes (specified by the label_metadata key)

Default values are *time_mode = 'framewise'* and *data_mode = 'value'*

See : :func:`timeside.analyzer.core.AnalyzerResult`, :class:`timeside.analyzer.core.AnalyzerResult`

Default
=======

Create a new analyzer result without default arguments

   >>> from timeside.analyzer.core import AnalyzerResult
   >>> res = AnalyzerResult()


   >>> res.keys()
   ['id_metadata', 'data_object', 'audio_metadata', 'parameters']

   >>> for key,value in res.items():
   ...     print '%s : %s' % (key, value)
   ...
   id_metadata : {'description': '', 'author': '', 'res_uuid': '', 'version': '', 'date': '', 'proc_uuid': '', 'id': '', 'unit': '', 'name': ''}
   data_object : {'y_value': array([], dtype=float64), 'value': array([], dtype=float64), 'frame_metadata': {'blocksize': None, 'samplerate': None, 'stepsize': None}}
   audio_metadata : {'sha1': '', 'is_segment': None, 'uri': '', 'channels': None, 'start': 0, 'channelsManagement': '', 'duration': None}
   parameters : {}


Specification of time_mode
==========================
Four different time_mode can be specified :

- 'framewise' : Data are returned on a frame basis (i.e. with specified blocksize, stepsize and framerate)
- 'global' : A global data value is return for the entire audio item
- 'segment' : Data are returned on a segmnet basis (i.e. with specified start time and duration)
- 'event' :  Data are returned on a segment basis (i.e. with specified start time)


Framewise
---------

>>> res = AnalyzerResult(time_mode='framewise')
>>> res.data_object.keys()
['value', 'y_value', 'frame_metadata']


Global
------

No frame metadata information is needed for these modes.
The 'frame_metadata' key/attribute is deleted.

>>> res = AnalyzerResult(time_mode='global')
>>> res.data_object.keys()
['value', 'y_value']

>>> res.data_object
GlobalValueObject(value=array([], dtype=float64), y_value=array([], dtype=float64))


Segment
-------

>>> res = AnalyzerResult(time_mode='segment')
>>> res.keys()
['id_metadata', 'data_object', 'audio_metadata', 'parameters']
>>> res.data_object
SegmentValueObject(value=array([], dtype=float64), y_value=array([], dtype=float64), time=array([], dtype=float64), duration=array([], dtype=float64))

Event
-----

>>> res = AnalyzerResult(time_mode='event')
>>> res.keys()
['id_metadata', 'data_object', 'audio_metadata', 'parameters']
>>> res.data_object
EventValueObject(value=array([], dtype=float64), y_value=array([], dtype=float64), time=array([], dtype=float64))

Specification of data_mode
==========================
Two different data_mode can be specified :

- 'value' : Data are returned as numpy Array of arbitrary type
- 'label' : Data are returned as label indexes (specified by the label_metadata key)

Value
-----

>>> res = AnalyzerResult(data_mode='value')
>>> res.data_object.keys()
['value', 'y_value', 'frame_metadata']

In the dataObject key, the 'value' key is kept and the 'label' key is deleted.

>>> res.data_object
FrameValueObject(value=array([], dtype=float64), y_value=array([], dtype=float64), frame_metadata=FrameMetadata(samplerate=None, blocksize=None, stepsize=None))

Label
-----
A *label_metadata* key is added.

>>> res = AnalyzerResult(data_mode='label')
>>> res.data_object.keys()
['label', 'label_metadata', 'frame_metadata']

>>> res.data_object
FrameLabelObject(label=array([], dtype=int64), label_metadata=LabelMetadata(label={}, description={}, label_type='mono'), frame_metadata=FrameMetadata(samplerate=None, blocksize=None, stepsize=None))
