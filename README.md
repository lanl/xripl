# XRIPL

[![Documentation Status](https://readthedocs.org/projects/xripl/badge/?version=latest)](https://xripl.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://xripl.readthedocs.io/en/latest/license.html)
[![GitHub Actions — CI](https://github.com/lanl/xripl/workflows/CI/badge.svg)](https://github.com/lanl/xripl/actions?query=workflow%3ACI+branch%3Amain)
[![codecov](https://codecov.io/gh/lanl/xripl/branch/main/graph/badge.svg)](https://codecov.io/gh/lanl/xripl)
[![GitHub Actions — Style linters](https://github.com/lanl/xripl/workflows/Style%20linters/badge.svg)](https://github.com/lanl/xripl/actions?query=workflow%3AStyle-linters+branch%3Amain)

XRIPL (C22023): X-Ray Radiographic Image Processing Library

Pawel M. Kozlowski 2018-10-19


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

## Installation
[Official releases of XRIPL](https://pypi.org/project/xripl/) are published to pypi.org and can simply be pip installed like so:
```
pip install xripl
```

More detailed installation instructions can be found [here](https://xripl.readthedocs.io/en/latest/install.html).


## License
XRIPL is released under a [3-clause BSD license](https://xripl.readthedocs.io/en/latest/license.html).

## Citing XRIPL
If you use XRIPL in your work, please follow the best practices for citing
XRIPL which can be found [here](https://xripl.readthedocs.io/en/latest/citing.html).

## Acknowledgements
Development of Fiducia was supported by the U.S. Department of Energy, and
the NNSA.
