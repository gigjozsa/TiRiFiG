================================================
TiRiFiG: A graphical 3D kinematic modelling tool
================================================

|PyPI Version|


TiRiFiC_ is a 3D kinematic modelling tool used to model resolved spectroscopic
observations of rotating discs in terms of the tilted-ring model with varying complexity.
The front-end (TiRiFiG, Tilted-Ring-Fitting-GUI), part of the toolkit, is an aid to
enable the user to perform the modelling process interactively.

.. |PyPI Version| image:: https://img.shields.io/badge/pypi-beta-orange.svg
                  :target: https://pypi.org/project/TiRiFiG/
                  :alt:

.. _PEP8: https://www.python.org/dev/peps/pep-0008/
.. _source: https://github.com/gigjozsa/TiRiFiG
.. _license: https://github.com/gigjozsa/TiRiFiG/blob/master/LICENSE
.. _TiRiFiC: http://gigjozsa.github.io/tirific/
.. _website: https://www.riverbankcomputing.com/software/pyqt/download

============
Requirements
============

The code requires full installation of:

.. code-block:: bash
  
    PyQt4
    TiRiFiC

============
Installation
============

Installation from source_, working directory where source is checked out

.. code-block:: bash
  
    $ pip install .

This package is available on *PYPI*, allowing

.. code-block:: bash
  
    $ pip install TiRiFiG

TiRiFiG depends on PyQt4 and TiRiFiC_ to run. To install PyQt4, I suggest installing Anaconda first and then installing PyQt4 using 
``conda install pyqt=4``. Alternatively, you can install it by following the instructions on the Riverbank Computing website_.

Download and installation notes for TiRiFiC_ is on its website. Once installed, add TiRiFiG to your PYTHONPATH using 
``export PATH='path_to_installation_directory:$PATH'``.

=====
Usage
=====

Start TiRiFiG, from the terminal.

With the GUI running, the next steps are:

- Click 'Open' and select a .def file to load and visualise.

- Adjust data points for the parameter(s) using the mouse.

- Start TiRiFiC from run menu to perform fitting.

=======
License
=======

This project is licensed under the MIT License - see license_ for details.

==========
Contribute
==========

Contributions are always welcome! Please ensure that you adhere to PEP8_ coding style guide.