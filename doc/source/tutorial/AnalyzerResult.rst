.. This file is part of TimeSide
   @author: Thomas Fillon

==========================
 Analyzer Result examples
==========================

Example of use of the Analyzer Result structure

Usage : AnalyzerResult.factory(data_mode=None, time_mode=None)

Four different *time_mode* can be specified :

- 'framewise' : Data are returned on a frame basis (i.e. with specified blocksize, stepsize and framerate)
- 'global' : A global data value is return for the entire audio item
- 'segment' : Data are returned on a segmnet basis (i.e. with specified start time and duration)
- 'event' :  Data are returned on a segment basis (i.e. with specified start time)

Two different *data_mode* can be specified :

- 'value' : Data are returned as numpy Array of arbitrary type
- 'label' : Data are returned as label indexes (specified by the label_metadata key)


See : :func:`timeside.analyzer.core.AnalyzerResult`, :class:`timeside.analyzer.core.AnalyzerResult`

Default
=======

Create a new analyzer result without arguments

   >>> from timeside.analyzer.core import AnalyzerResult
   >>> res = AnalyzerResult.factory()

This default result has all the metadata and dataObject attribute

   >>> res.keys()
   ['id_metadata', 'data_object', 'audio_metadata', 'frame_metadata', 'parameters']

   >>> for key,value in res.items():
   ...     print '%s : %s' % (key, value)
   ...
   id_metadata : {'description': '', 'author': '', 'uuid': '', 'version': '', 'date': '', 'id': '', 'unit': '', 'name': ''}
   data_object : {'value': array([], dtype=float64)}
   audio_metadata : {'sha1': '', 'is_segment': None, 'uri': '', 'channels': None, 'start': 0, 'channelsManagement': '', 'duration': None}
   frame_metadata : {'blocksize': None, 'samplerate': None, 'stepsize': None}
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

>>> res = AnalyzerResult.factory(time_mode='framewise')
>>> res.keys()
['id_metadata', 'data_object', 'audio_metadata', 'frame_metadata', 'parameters']

Global
------

No frame metadata information is needed for these modes.
The 'frame_metadata' key/attribute is deleted.

>>> res = AnalyzerResult.factory(time_mode='global')
>>> res.keys()
['id_metadata', 'data_object', 'audio_metadata', 'parameters']
>>> res.data_object
DataObject(value=array([], dtype=float64))

Segment
-------

>>> res = AnalyzerResult.factory(time_mode='segment')
>>> res.keys()
['id_metadata', 'data_object', 'audio_metadata', 'parameters']
>>> res.data_object
DataObject(value=array([], dtype=float64), time=array([], dtype=float64), duration=array([], dtype=float64))

Event
-----

>>> res = AnalyzerResult.factory(time_mode='event')
>>> res.keys()
['id_metadata', 'data_object', 'audio_metadata', 'parameters']
>>> res.data_object
DataObject(value=array([], dtype=float64), time=array([], dtype=float64))

Specification of data_mode
==========================
Two different data_mode can be specified :

- 'value' : Data are returned as numpy Array of arbitrary type
- 'label' : Data are returned as label indexes (specified by the label_metadata key)

Value
-----
The label_metadata key is deleted.

>>> res = AnalyzerResult.factory(data_mode='value')
>>> res.keys()
['id_metadata', 'data_object', 'audio_metadata', 'frame_metadata', 'parameters']

In the dataObject key, the 'value' key is kept and the 'label' key is deleted.

>>> res.data_object
DataObject(value=array([], dtype=float64))

Label
-----
>>> res = AnalyzerResult.factory(data_mode='label')
>>> res.keys()
['id_metadata', 'data_object', 'audio_metadata', 'frame_metadata', 'label_metadata', 'parameters']

In the dataObject key, the 'label' key is kept and the 'value' key is deleted.


>>> res.data_object
DataObject(label=array([], dtype=int64))
