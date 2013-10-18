.. This file is part of TimeSide
   @author: Thomas Fillon

Analyzer Result example
=============================

Example of use of the new analyzerResult structure

Usage : AnalyzerResult(data_mode=None, time_mode=None)

See : :class:`timeside.analyzer.core.AnalyzerResult`

Default
=======

Create a new analyzer result without arguments

   >>> from timeside.analyzer.core import AnalyzerResult
   >>> res = AnalyzerResult()

This default result has all the metadata and dataObject attribute

   >>> res.keys()
   ['data_mode', 'time_mode', 'id_metadata', 'data', 'audio_metadata', 'frame_metadata', 'label_metadata', 'parameters']

   >>> for key,value in res.items():
   ...     print '%s : %s' % (key, value)
   ...
   data_mode : None
   time_mode : None
   id_metadata : {'description': '', 'author': '', 'version': '', 'date': '', 'id': '', 'unit': '', 'name': ''}
   dataObject : {'duration': array([], dtype=float64), 'time': array([], dtype=float64), 'value': None, 'label': array([], dtype=int64)}
   audio_metadata : {'duration': None, 'start': 0, 'channelsManagement': '', 'uri': '', 'channels': None}
   frame_metadata : {'blocksize': None, 'samplerate': None, 'stepsize': None}
   label_metadata : {'label_type': 'mono', 'description': None, 'label': None}
   parameters : {}


Specification of time_mode
=========================
Four different time_mode can be specified :

- 'framewise' : Data are returned on a frame basis (i.e. with specified blocksize, stepsize and framerate)
- 'global' : A global data value is return for the entire audio item
- 'segment' : Data are returned on a segmnet basis (i.e. with specified start time and duration)
- 'event' :  Data are returned on a segment basis (i.e. with specified start time)


Framewise
---------

>>> res = AnalyzerResult(time_mode='framewise')
>>> res.keys()
['data_mode', 'time_mode', 'id_metadata', 'data', 'audio_metadata', 'frame_metadata', 'label_metadata', 'parameters']

Global
------

No frame metadata information is needed for these modes.
The 'frame_metadata' key/attribute is deleted.

>>> res = AnalyzerResult(time_mode='global')
>>> res.keys()
['data_mode', 'time_mode', 'id_metadata', 'data', 'audio_metadata', 'label_metadata', 'parameters']
>>> res.data_object
DataObject(value=None, label=array([], dtype=int64))

Segment
-------

>>> res = AnalyzerResult(time_mode='segment')
>>> res.keys()
['data_mode', 'time_mode', 'id_metadata', 'data', 'audio_metadata', 'label_metadata', 'parameters']
>>> res.data
DataObject(value=None, label=array([], dtype=int64), time=array([], dtype=float64), duration=array([], dtype=float64))

Event
-----

>>> res = AnalyzerResult(time_mode='event')
>>> res.keys()
['data_mode', 'time_mode', 'id_metadata', 'data', 'audio_metadata', 'label_metadata', 'parameters']
>>> res.data
DataObject(value=None, label=array([], dtype=int64), time=array([], dtype=float64))

Specification of data_mode
=========================
Two different data_mode can be specified :

- 'value' : Data are returned as numpy Array of arbitrary type
- 'label' : Data are returned as label indexes (specified by the label_metadata key)

Value
-----
The label_metadata key is deleted.

>>> res = AnalyzerResult(data_mode='value')
>>> res.keys()
['data_mode', 'time_mode', 'id_metadata', 'data', 'audio_metadata', 'frame_metadata', 'parameters']

In the dataObject key, the 'value' key is kept and the 'label' key is deleted.

>>> res.data
DataObject(value=None, time=array([], dtype=float64), duration=array([], dtype=float64))

Label
-----
>>> res = AnalyzerResult(data_mode='label')
>>> res.keys()
['data_mode', 'time_mode', 'id_metadata', 'data', 'audio_metadata', 'frame_metadata', 'label_metadata', 'parameters']

In the dataObject key, the 'label' key is kept and the 'value' key is deleted.


>>> res.data
DataObject(label=array([], dtype=int64), time=array([], dtype=float64), duration=array([], dtype=float64))
