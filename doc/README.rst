========
 README
========

Installation
============

To build *TimeSide* documentation, you need first to install *Sphinx* and its *numpydoc* extension.


Installing Sphinx
-----------------
For more complete instructions to install Sphinx on every platform see http://sphinx-doc.org/latest/install.html


Debian/Ubuntu: Install Sphinx using packaging system
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You may install using this command if you use Debian/Ubuntu.

.. code-block:: bash

   $ apt-get install python-sphinx

Installing Sphinx with easy_install
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have *easy-install* on your system you can install Sphinx with:

.. code-block:: bash

   $ easy_install sphinx

After installation, type ``sphinx-build`` on the command prompt.  If
everything worked fine, you will get a Sphinx version number and a list of
options for this command.


Installing Sphinx extension Numpydoc
------------------------------------
*Numpydoc* is a Sphinx extension to support docstrings in Numpy format
see https://pypi.python.org/pypi/numpydoc

It can be *easilly install* with:

.. code-block:: bash

   $ easy_install numpydoc


Building the doc
================

From the ``doc`` directory, you need to run the following command to generate the HTML docs in the ``build`` directory:

.. code-block:: bash

   $ make html


*Doctest* can be performed by:

.. code-block:: bash

   $ make doctest
