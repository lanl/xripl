#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 16:11:09 2019

XRIPL setup script.

@author: Pawel M. Kozlowski
"""

from setuptools import setup

# Read the contents of the README file to include in the long
# description. The long description then becomes part of the pypi.org
# page.
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='xripl',
      version='0.2.0',
      description='X-Ray Radiographic Image Processing Library',
      long_description=long_description,
      long_description_content_type='text/markdown',
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