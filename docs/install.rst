 .. _install:

*******************
Installing XRIPL
*******************

Requirements
============

XRIPL requires Python version 3.7 or newer.
XRIPL also require the following openly available packages for installation:


- `NumPy <https://www.numpy.org/>`_ — 1.15.0 or newer
- `matplotlib <https://matplotlib.org/>`_ — 2.2.2 or newer
- `scipy <https://scipy.org/>`_ — 1.1.0 or newer
- `h5py <https://www.h5py.org/>`_ — 2.8.0 or newer
- `scikit-image <https://scikit-image.org/>`_ — 0.14.0 or newer

Installation with pip
=====================
`Official releases of XRIPL <https://pypi.org/project/xripl/>`_ are
published to `pypi.org <https://pypi.org/>`_ and can simply be pip installed
like so:

.. code-block:: python

   pip install xripl


Building and installing from source (for contributors)
======================================================
Make sure you have python installed, preferably via Anaconda
------------------------------------------------------------
Here is where you get Anaconda, and make sure to get the Python 3 version.
https://www.anaconda.com/distribution/

Setup installation directory
----------------------------
Make a directory called "xripl" in a sensible place on your system. Preferably in a directory where none of the higher level directory names have spaces in them.

Setup a virtual environment
---------------------------
If you have python installed via Anaconda, then create your virtual environment like this

.. code-block:: bash

   conda create --name xripl


Clone the repository using git
------------------------------
In the xripl directory you created, run the following on the command line

.. code-block:: bash

   git clone https://github.com/lanl/xripl.git


Activate your virtual environment
---------------------------------
Still on the command line, run

.. code-block:: bash

   source activate xripl


Install requirements
--------------------

.. code-block:: bash

   pip install -r requirements.txt


Install xripl
---------------
If you are a user then do

.. code-block:: bash

   pip install .


If you wish to help in developing xripl, then do

.. code-block:: bash

   pip install -e .


Test if install was successful
------------------------------
Open a python and try doing ``import xripl``. If all went well then you shouldn't get any error messages.
