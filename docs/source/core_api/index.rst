=================
TimeSide core API
=================

TimeSide is first a python framework enabling low and high level audio analysis, imaging, transcoding, streaming and labelling. Its high-level API is designed to enable complex processing on very large datasets of any audio or video assets with a plug-in architecture, a secure scalable backend and an extensible dynamic web frontend. Some usecases: scaled audio computing (filtering, machine learning, etc), web audio visualization, audio process prototyping, realtime and on-demand transcoding and streaming over the web, automatic segmentation and labelling synchronized with audio events

Because there are a lot of tools available in the Python ecosystem dedicated to music information retrieval, machine learning and data analysis, we have decided to embed all main ones: Aubio\cite{aubio}, Yaafe\cite{yaafe_ISMIR2010}, Essentia\cite{essentia}, VAMP\cite{vamp-plugins}, librosa\cite{librosa}, GStreamer, TensorFlow, Torch, PyTorch, scikit-learn, Jupyter, Pandas and Pytables. They are used to develop native TimeSide plugins though its simple processing API.


.. toctree::
   :maxdepth: 2

   processors_list/processors_list
   decoder/index
   analyzer/index
   encoder/index
   grapher/index
   provider/index
