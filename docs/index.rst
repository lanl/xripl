.. xripl documentation master file, created by
   sphinx-quickstart on Wed Jun  1 13:57:10 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

XRIPL's Documentation
=================================

XRIPL (read as "zripple") is a library of tools for processing x-ray
radiographs and extracting contours of interest within the image using
computer vision techniques. Features include spatial calibration, denoising,
background and attenuation correction through pseudo-flatfielding, watershed
segmentation, contour processing, and visualization. The details of the XRIPL
analysis pipeline are published in the Proceedings of the 23rd Topical
Conference on High-Temperature Plasma Diagnostics Proceedings [1].

[1] P. M. Kozlowski, Y. Kim, B. M. Haines, H. F. Robey, T. J. Murphy,
H. M. Johns, and T. S. Perry. Use of Computer Vision for analysis of image
data sets from high temperature plasma experiments. Review of Scientific
Instruments 92, 033532 (2021) https://doi.org/10.1063/5.0040285

.. toctree::
   :caption: First Steps
   :maxdepth: 1

   Installing <install>
   Examples <auto_examples/index>
   Contributing <contributing>
   Citing <citing>
   License <license>

.. toctree::
   :maxdepth: 1
   :caption: Submodules

   clean
   contour
   contrast
   films
   filters
   instrument
   magnification
   pltDefaults
   reader
   segmentation
   tubeTransmission
   visualizations
 

.. _toplevel-development-guide:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
