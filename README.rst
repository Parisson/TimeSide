TimeSide : scalable audio processing framework and server written in Python
===========================================================================

TimeSide is a Python framework enabling low and high level audio analysis, imaging, transcoding, streaming and labelling. Its high-level API is designed to enable complex processing on very large datasets of any audio or video assets with a plug-in architecture and a secured scalable backend.


Introduction
=============

As the number of online audio applications and datasets increase, it becomes crucial for researchers and engineers to be able to prototype and test their own algorithms as fast as possible on various platforms and usecases like computational musicology and streaming services. On the other side, content providers and producers need to enhance user experiences on their platforms with more metadata based on cultural history but also audio feature analyses. Growing those metadata synchronously with the music published on the internet implies that the analysis and storage systems can be easily updated, scaled and deployed.

TimeSide has been developed in this sense to propose an online audio processing service. It provides:

- a **core module** for Python to work from a shell or any other Python based program
- a **web server** for the Web with a RESTful API built on top of the core module so that web developers can then easily embed the remote processing service into their own applications.
- a **SDK** for Javascript and based on OpenAPI to easily develop a third party application consuming the server API.


Use cases
==========

- Asynchronous audio processing (filtering, feature analysis, machine learning, etc)
- Scaled and secured data provisioning, processing and accessing
- Audio plugin prototyping
- Audio visualization
- On-demand transcoding and streaming over the Web
- Enhanced shared audio player
- Automatic segmentation and manual labelling synchronized with audio events


Features
========

- **Do** asynchronous and fast audio processing with Python,
- **Decode** audio frames from **any** audio or video media format into numpy arrays,
- **Analyze** audio content with some state-of-the-art audio feature extraction libraries like Aubio, Yaafe and VAMP as well as some pure python processors
- **Visualize** sounds with various fancy waveforms, spectrograms and other cool graphers,
- **Transcode** audio data in various media formats and stream them through web apps,
- **Serialize** feature analysis data through various portable formats,
- **Provide** audio sources from plateform like YouTube or Deezer
- **Deliver** analysis and transcode on provided or uploaded tracks over the web through a REST API
- **Playback** and **interact** **on demand** through a smart high-level HTML5 extensible player,
- **Index**, **tag** and **annotate** audio archives with semantic metadata (see `Telemeta <http://telemeta.org>`__ which embed TimeSide).
- **Deploy** and **scale** your own audio processing engine through any infrastructure


Funding and support
===================

To fund the project and continue our fast development process, we need your explicit support. So if you use TimeSide in production or even in a development or experimental setup, please let us know by:

- staring or forking the project on `GitHub <https://github.com/Ircam-WAM/TimeSide>`_
- droping us an email at <wam@ircam.fr>

Thanks for your help and support!

News
=====

1.1
---

- Core:

  - Use the libav based aubio decoder by default (fastest audio to numpy array converter on the planet!)
  - Add a VAMP based analyzer and a few plugins like VampFlatness, VampCrest, VampTempo, VampTuning, VampSpectralCentroid, VampSpectralKurtosis and VampSpectralSlope

- Server:

  - Fix a lot of asynchronous processing issues: now do every pre-processing, processing and post-processing tasks through the worker including source stream fetching from youtube
  - Add a process monitor based on websocket
  - Waveform automatically processed on Item.save()
  - Make UUID really unique
  - Reordering models
  - Improve unit tests


1.0
---

* Server refactoring:

  * audio process run on items (REST API track's model)
  * several tools, views, models and serializers
  * REST API's schema on OpenAPI 3 specification and automatic Redoc generation

* Move core and server from Python 2.7 to 3.7
* Upgrade Django to 2.2, Django REST Framework to 3.11, Celery to 4.4
* Add an `Aubio <https://github.com/aubio/aubio>`_ based decoder
* Add core and server processors' versioning and server process' run time
* Regroup all dependencies on pip requirements removing conda use
* Add Provider class as a core API component and as a REST API model
* Add provider plugins deezer-preview, deezer-complete and youtube
* Improve server unit testing
* Add JWT authentication on REST API
* Various bug fixes
* Add core, server and workers logging


0.9
---

* Upgrade all python dependencies
* Add Vamp, Essentia, Yaafe, librosa, PyTorch, Tensorflow libs and wrappers
* Add a few analyzing plugins (Essentia Dissonance, Vamp Constant Q, Vamp Tempo, Vamp general wrapper, Yaafe general wrapper)
* Add processor parameter management
* Add processor inheritance
* Improve HTML5 player with clever data streaming
* Improve REST API and various serialzers
* Improve unit testing
* Various bug fixes

0.8
---

* Add *Docker* support for instant installation. This allows to run TimeSide now on *any* OS platform!
* Add `Jupyter Notebook <http://jupyter.org/>`_ support for easy prototyping, experimenting and sharing (see the examples in the doc).
* Add an experimental web server and REST API based on Django REST Framework, Redis and Celery. This now provides a real web audio processing server with high scaling capabilities thanks to Docker (clustering) and Celery (multiprocessing).
* Start the development of a new player interface thanks to Angular and WavesJS.
* Huge cleanup of JS files. Please now use bower to get all JS dependencies as `listed in settings <https://github.com/Ircam-WAM/TimeSide/blob/dev/app/sandbox/settings.py#L199>`_.
* Add metadata export to Elan annotation files.
* Fix and improve some data structures in analyzer result containers.
* Many various bugfixes.

0.7.1
-----

* fix django version to 1.6.10 (sync with Telemeta 1.5)

0.7
----

* Code refactoring:

  * Create a new module `timeside.plugins` and move processors therein: timeside.plugins.decoder,analyzer, timeside.plugins.encoder, timeside.plugins.fx
  * WARNING: to properly manage the namespace packages structure, the TimeSide main module is now `timeside.core` and code should now be initialized with `import timeside.core`
  * `timeside.plugins` is now a `namespace package <https://pythonhosted.org/setuptools/setuptools.html#namespace-packages>`_ enabling external plugins to be **automatically** plugged into TimeSide (see for example `timeside-diadems <https://github.com/ANR-DIADEMS/timeside-diadems>`_). This now makes TimeSide a **real** plugin host, yeah!
  * A dummy timeside plugin will soon be provided for easy development start.

* Move all analyzers developped by the partners of the Diadems project to a new repository: `timeside-diadems <https://github.com/ANR-DIADEMS/timeside-diadems>`_
* Many fixes for a better processing by `Travis-CI <https://travis-ci.org/Ircam-WAM/TimeSide>`_
* Add a dox file to test the docker building continously on `various distributions <https://github.com/Parisson/Docker>`_

For older news, please visit: https://github.com/Ircam-WAM/TimeSide/blob/master/NEWS.rst

Documentation
==============

- Full documentation: https://timeside.ircam.fr/docs/
- Server REST API: https://timeside.ircam.fr/api/docs/
- Slides: https://ircam-wam.github.io/timeside-slides/#1
- Core tutorials: https://timeside.ircam.fr/docs/tutorials/
- Some notebooks: https://github.com/Ircam-WAM/TimeSide/tree/master/docs/ipynb
- Some older notebooks: http://mybinder.org/repo/thomasfillon/Timeside-demos
- Publications:

  - https://github.com/Parisson/Telemeta-doc
  - https://github.com/Ircam-WAM/timeside-papers

- Player UI v2: https://github.com/Ircam-WAM/timeside-player
- Player UI v1 guide: https://github.com/Ircam-WAM/TimeSide/wiki/Ui-Guide
- Player UI v1 example: http://archives.crem-cnrs.fr/archives/items/CNRSMH_E_2004_017_001_01/

Install
=======

Thanks to Docker, Timeside is now fully available as a docker composition ready to work. The docker based composition bundles some powerful applications and modern frameworks out-of-the-box like: Python, Numpy, Jupyter, Gstreamer, Django, Celery, PostgreSQL, Redis, uWSGI, Nginx and more.

First, install `Docker <https://docs.docker.com/get-docker/>`_ and `docker compose <https://docs.docker.com/compose/install/>`_

Then clone TimeSide and start it up::

    git clone --recursive https://github.com/Ircam-WAM/TimeSide.git
    cd TimeSide
    docker compose up -d

That's it! Now please go to the :ref:`User Interfaces` section to see how to use it.

.. note::
   To get technical support, please reach the development team. If you need to use TimeSide *outside* a docker image please refer to the rules of the Dockerfile which is based on a Debian stable system. We will NOT provide any kind of free support in this paticular usecase outside the original docker container.

Sponsors and Partners
=====================

- `IRCAM <https://www.ircam.fr>`_ (Paris, France)
- `Parisson <http://parisson.com>`_ (Paris, France)
- `CNRS <http://www.cnrs.fr>`_: National Center of Science Research (France)
- `Huma-Num <http://www.huma-num.fr/>`_: big data equipment for digital humanities (CNRS, France)
- `CREM <http://www.crem-cnrs.fr>`_: French National Center of Ethomusicology Research (France)
- `Université Pierre et Marie Curie <http://www.upmc.fr>`_ (UPMC Paris, France)
- `ANR <http://www.agence-nationale-recherche.fr/>`_: Agence Nationale de la Recherche (France)
- `MNHN <http://www.mnhn.fr>`_ : Museum National d'Histoire Naturelle (Paris, France)
- `C4DM <http://c4dm.eecs.qmul.ac.uk/>`_ : Center for Digital Music, Queen Mary University (London, United Kingdom)
- `NYU Steinhardt <http://steinhardt.nyu.edu/music/>`_ : Music and Performing Arts Professions, New York University (New York, USA)

Related projects
=================

- `Telemeta <http://telemeta.org>`__ : Open web audio platform
- `Sound archives of the CNRS <http://archives.crem-cnrs.fr/>`_, CREM and the "Musée de l'Homme" in Paris, France
- `DIADEMS <http://www.irit.fr/recherches/SAMOVA/DIADEMS/en/welcome/>`_ sponsored by the ANR.
- `DaCaRyh <http://gtr.rcuk.ac.uk/projects?ref=AH/N504531/1>`_, Data science for the study of calypso-rhythm through history
- `KAMoulox <https://anr-kamoulox.github.io/>`_ Online unmixing of large historical archives
- NYU+CREM+Parisson : arabic music analysis from the full CREM database
- `WASABI <http://wasabihome.i3s.unice.fr/>`_: Web Audio Semantic Aggregated in the Browser for Indexation, sponsored by the ANR
- `timeside-player v2 <https://github.com/Ircam-WAM/timeside-player>`_
- `timeside-sdk-js <https://github.com/Ircam-WAM/timeside-sdk-js>`_
References
==========

- Aline Menin, Michel Buffa, Maroua Tikat, Benjamin Molinet, Guillaume Pellerin, Laurent Pottier, Franck Michel, & Marco Winckler. (2022, June 28). Incremental and multimodal visualization of discographies: exploring the WASABI music knowledge base. Web Audio Conference 2022 (WAC 2022), Cannes, France. https://doi.org/10.5281/zenodo.6767530
- Guillaume Pellerin, & Paul Brossier. (2022). TimeSide API as an audio processing web service [Data set]. Web Audio Conference 2022 (WAC 2022), Cannes, France. Zenodo. https://doi.org/10.5281/zenodo.6769477
- T. Fillon and G. Pellerin. A collaborative web platform for sound archives management and analysis. In Proceedings of 3rd Web Audio Conference, London, page 43. Queen Mary University of London, August 2017.

Copyrights
==========

- Copyright (c) 2019, 2023 IRCAM
- Copyright (c) 2006, 2023 Guillaume Pellerin
- Copyright (c) 2022, 2023 Guillaume Piccarreta
- Copyright (c) 2010, 2022 Paul Brossier
- Copyright (c) 2020, 2021 Romain Herbelleau
- Copyright (c) 2019, 2020 Antoine Grandry
- Copyright (c) 2006, 2019 Parisson SARL
- Copyright (c) 2013, 2017 Thomas Fillon
- Copyright (c) 2013, 2014 Maxime Lecoz
- Copyright (c) 2013, 2014 David Doukhan
- Copyright (c) 2006, 2010 Olivier Guilyardi


License
=======

TimeSide is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

TimeSide is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

Read the `LICENSE.txt <https://github.com/Ircam-WAM/TimeSide/blob/master/LICENSE.txt>`_ file for more details.
