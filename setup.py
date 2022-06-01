#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 16:11:09 2019

XRIPL setup script.

@author: Pawel M. Kozlowski
"""

from setuptools import setup

setup(name='xripl',
      version='0.1',
      description='X-Ray Radiographic Image Processing Library',
      url='https://github.com/lanl/xripl',
      author='Pawel Marek Kozlowski',
      author_email='pkozlowski@lanl.gov',
      license='BSD',
      classifiers=['Intended Audience :: Science/Research',
                   'License :: OSI Approved :: BSD License',
                   'Development Status :: 3 - Alpha',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 3',
                   'Topic :: Scientific/Engineering :: Physics',
                   'Topic :: Scientific/Engineering :: Image Processing',
                   'Natural Language :: English'],
      packages=['xripl'],
      zip_safe=False)