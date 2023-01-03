=================
Core API
=================

TimeSide is first a python framework enabling low and high level audio analysis, imaging, transcoding, streaming and labelling. Its high-level API is designed to enable complex processing on very large datasets of any audio or video assets with a plug-in architecture, a secure scalable backend and an extensible dynamic web frontend. Some usecases: scaled audio computing (filtering, machine learning, etc), web audio visualization, audio process prototyping, realtime and on-demand transcoding and streaming over the web, automatic segmentation and labelling synchronized with audio events

Because there are a lot of tools available in the Python ecosystem dedicated to music information retrieval, machine learning and data analysis, we have decided to embed all main ones: Aubio, Yaafe, Essentia, VAMP, librosa, GStreamer, TensorFlow, Torch, PyTorch, scikit-learn, Jupyter, Pandas and Pytables. They are used to develop native TimeSide plugins though its simple processing API.

The Pipe
=========

The framework is based on a streaming architecure where each block can be process by each plugin. As a result, the data can be stored afterwards in various formats.

The following diagram shows and example of a pipe.

.. image:: ../images/TimeSide_pipe.svg
  :width: 800 px


Classes
========

.. toctree::
   :maxdepth: 2

   processors_list/processors_list
   decoder/index
   analyzer/index
   encoder/index
   grapher/index
   provider/index
