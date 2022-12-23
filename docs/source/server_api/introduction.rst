Introduction
=============

In addition to be usable as a library, TimeSide has furthermore been built into a Django server with a relational PostgreSQL database in order to store music tracks and processing results. Data structure and relations are defined in the models to ensure easy data serialization. The backend is built with Django REST Framework to provide a documented RESTful API. It guarantees interoperability by allowing other servers or multiple frontends to interact with the TimeSide instance. Any application consuming the API is then able to:

- upload audio track or retrieve them from remote providers
- stream original or transcoded sources
- run on-demand analysis with customized parameters
- deliver and share several types of results: transcoded audio, numerical or graphical outputs of analysis,
- collect tags and indices on tracks to build annotated audio corpora for further machine learning purpose.

Models and Serializers
-----------------------

The models of the backend are defined as usual Django models and are all stored with a UUID. Here is a list of the main ones:

- Item: a resource with a source file or URL
- Selection: a list of Items
- Processor: a versioned TimeSide Processor
- Preset: a Processor with some parameters in the JSON format
- Experience: a list of Presets
- Task: a list of Selection linked to an Experience to run

This modelization allows to define some specific precessing \textit{Experiences} that can be re-processed on any new \textit{Selection} which is espacially convenient for analysis on growing datasets. All model instances and related data are accesible through a REST API with authentication. This ensures that a client can consume TimeSide as a dedicated and autonomous web service.

The API full documentation is there: https://timeside.ircam.fr/timeside/api/docs/


Results and Formats
--------------------

All processing results are accesible in a \verb|AnalyzerResult| python object containing a structured and documented data dictionary which can be serialized, stored and restored in HDF5, JSON, YAML or XML formats. The file contains all the preset parameters and data structure so that, if a process is requested for the same media file, same processors type and same version, the data will be automatically retrieve from the databasen and eventualluy re-processed in another child processor or serializer. The TimeSide server also embeds a full relational database to store any lighter data that has be be linked to models.