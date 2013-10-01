.. This file is part of TimeSide
   @author: Thomas Fillon

=============================
 New analyzer Result example
=============================

Example of use of the new analyzerResult structure

Usage : newAnalyzerResult(dataMode=None, timeMode=None)

See : :class:`timeside.analyzer.core.newAnalyzerResult`

Default
=======

Create a new analyzer result without arguments

   >>> import timeside.analyzer.core as coreA
   >>> res = coreA.newAnalyzerResult()

This default result has all the metadata and data attribute

   >>> res.keys()
   ['dataMode', 'timeMode', 'idMetadata', 'data', 'audioMetadata', 'frameMetadata', 'labelMetadata', 'parameters']

   >>> for key,value in res.items():
   ...     print '%s : %s' % (key, value)
   ...
   dataMode : None
   timeMode : None
   idMetadata : {'description': '', 'author': '', 'version': '', 'date': '', 'id': '', 'unit': '', 'name': ''}
   data : {'duration': array([], dtype=float64), 'time': array([], dtype=float64), 'value': None, 'label': array([], dtype=int64)}
   audioMetadata : {'duration': None, 'start': 0, 'channelsManagement': '', 'uri': '', 'channels': None}
   frameMetadata : {'blocksize': None, 'samplerate': None, 'stepsize': None}
   labelMetadata : {'labelType': 'mono', 'description': None, 'label': None}
   parameters : {}


Specification of timeMode
=========================
Four different timeMode can be specified :

- 'framewise' : Data are returned on a frame basis (i.e. with specified blocksize, stepsize and framerate)
-  'global' : A global data value is return for the entire audio item
-  'segment' : Data are returned on a segmnet basis (i.e. with specified start time and duration)
-  'event' :  Data are returned on a segment basis (i.e. with specified start time)


Framewise
---------

>>> res = coreA.newAnalyzerResult(timeMode='framewise')
>>> res.keys()
['dataMode', 'timeMode', 'idMetadata', 'data', 'audioMetadata', 'frameMetadata', 'labelMetadata', 'parameters']

Global
------

No frame metadata information is needed for these modes.
The 'frameMetadata' key/attribute is deleted.

>>> res = coreA.newAnalyzerResult(timeMode='global')
>>> res.keys()
['dataMode', 'timeMode', 'idMetadata', 'data', 'audioMetadata', 'labelMetadata', 'parameters']
>>> res.data
AnalyzerData(value=None, label=array([], dtype=int64))

Segment
-------

>>> res = coreA.newAnalyzerResult(timeMode='segment')
>>> res.keys()
['dataMode', 'timeMode', 'idMetadata', 'data', 'audioMetadata', 'labelMetadata', 'parameters']
>>> res.data
AnalyzerData(value=None, label=array([], dtype=int64), time=array([], dtype=float64), duration=array([], dtype=float64))

Event
-----

>>> res = coreA.newAnalyzerResult(timeMode='event')
>>> res.keys()
['dataMode', 'timeMode', 'idMetadata', 'data', 'audioMetadata', 'labelMetadata', 'parameters']
>>> res.data
AnalyzerData(value=None, label=array([], dtype=int64), time=array([], dtype=float64))

Specification of dataMode
=========================
Two different dataMode can be specified :

- 'value' : Data are returned as numpy Array of arbitrary type
- 'label' : Data are returned as label indexes (specified by the labelMetadata key)

Value
-----
The labelMetadata key is deleted.

>>> res = coreA.newAnalyzerResult(dataMode='value')
>>> res.keys()
['dataMode', 'timeMode', 'idMetadata', 'data', 'audioMetadata', 'frameMetadata', 'parameters']

In the data key, the 'value' key is kept and the 'label' key is deleted.

>>> res.data
AnalyzerData(value=None, time=array([], dtype=float64), duration=array([], dtype=float64))

Label
-----
>>> res = coreA.newAnalyzerResult(dataMode='label')
>>> res.keys()
['dataMode', 'timeMode', 'idMetadata', 'data', 'audioMetadata', 'frameMetadata', 'labelMetadata', 'parameters']

In the data key, the 'label' key is kept and the 'value' key is deleted.


>>> res.data
AnalyzerData(label=array([], dtype=int64), time=array([], dtype=float64), duration=array([], dtype=float64))
