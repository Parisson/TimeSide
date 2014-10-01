=========================
 Saving TimeSide results
=========================

TimeSide results can be optionnaly saved to disk.
The saving process can be done automatically or manually and TimeSide results will be saved to HDF5_ files with h5py_ or Pytables_.

Nevertheless, results can also be manually serialized to the following formats:
 - JSON   (see :func:`timeside.analyzer.core.AnalyzerResultContainer.to_json`)
 - YAML    (see :func:`timeside.analyzer.core.AnalyzerResultContainer.to_yaml`)
 - XML    (see :func:`timeside.analyzer.core.AnalyzerResultContainer.to_xml`)
 - Numpy   (see :func:`timeside.analyzer.core.AnalyzerResultContainer.to_numpy`)
 - HDF5               (see :func:`timeside.analyzer.core.AnalyzerResultContainer.to_hdf5`)

.. _h5py: http://www.h5py.org/
.. _Pytables: http://www.pytables.org
.. _HDF5: http://www.hdfgroup.org/HDF5/

TimeSide working directory
==========================

To save the results of a given pipe, we need to specify a working directory.
The working directory is set with the :func:`set_working_directory` function and can be retrieved with the :func:`get_working_directory` function

>>> WORKING_DIR = '/tmp/TS'
>>> timeside.set_working_dir(WORKING_DIR)
>>> timeside.get_working_dir()
'/tmp/TS'

By default, the working directory is set to `None`.

To automatically save the results when running a process pipe you need to switch the autosaving parameter to `True`.

The autosaving parameter can be accessed and set respectivelly with the :func:`get_autosaving` and :func:`set_autosaving` functions.

>>> timeside.set_autosaving(True)
>>> timeside.get_autosaving()
True

>>> timeside.set_autosaving(False)
>>> timeside.get_autosaving()
False





HDF5 file hierarchy
-------------------
3 levels : 
 1. : The media item level
 2. : The decoder level: one group by set of decoder parameters
    Each decoder differs from the other by :
      - start
      - duration
      - samplerate
      - channels
      - blocksize ?
  3. : The results level : one group by result

.. digraph:: file_hierarchy

   file [label="file.h5\nSource=file.wav" shape=folder]
   file -> {dec1 dec2 dec3};
   dec1 [label="decoder 1\nSamplerate=44100" shape=folder];
   dec2 [label="decoder 2\nSamplerate=16000" shape=folder];
   dec3 [label="decoder 3\nDuration=30s" shape=folder];
   A [label="a.h5\nResult A" shape=folder];
   B [label="b.h5\nResult B" shape=folder];
   C [label="c.h5\nResult C" shape=folder];
   D [label="d.h5\nResult D" shape=folder];
   E [label="e.h5\nResult E" shape=folder];
   dec1 -> A [label="ext. link"];
   dec1 -> B [label="ext. link"];
   dec1 -> C [label="ext. link"];
   dec2 -> D [label="ext. link"];
   dec3 -> E [label="ext. link"];


HDF5 file/groups hierarchy example:
 | item.sha1
 | item.sha1/decoder_1.uuid
 | item.sha1/decoder_1.uuid/result_1.uuid
 | item.sha1/decoder_1.uuid/result_2.uuid
 | item.sha1/decoder_1.uuid/result_3.uuid
 | item.sha1/decoder_2.uuid
 | item.sha1/decoder_2.uuid/result_1.uuid


With
::
  >>> decoder = FileDecoder('path/to/item.wav')
  >>> decoder.sha1
  'a4ba8e700eeff426923c8f83b43b7ac22a6658b2'
  >>> decoder.uuid()
  'b8c29e29-0771-494a-a5f0-7ed44fd0e0db'

The result for this item with be save to WORKING_DIR/a4ba8e700eeff426923c8f83b43b7ac22a6658b2.h5

TimeSide Server view
--------------------
TIMESIDE_WORKING_DIR 
cf. server/sandbox/settings.py

- Item has a hdf5 field --> 
      
>>> item_path = os.path.join(results_path, item.uuid) # item.uuid inherited from BaseResource
>>> hdf5_file = str(self.experience.uuid) + '.hdf5'
>>> item.hdf5 =  os.path.join(item_path, hdf5_file)

- result has a hdf5 field:
>>> hdf5_file = str(result.uuid) + '.hdf5'  # result.uuid inherited from BaseResource
>>> result.hdf5 = os.path.join(item_path, hdf5_file)
 
 
Remaining Questions
-------------------
 - h5py or pytables ? --> plutôt Pytables mais il faudra chnager le code des AnalyzerResults
 - Do we need to separate the 3 levels in differents hdf5 files ? Given that it could be transparent for h5py or pytables given the "external link" features of both libraries ?

 

