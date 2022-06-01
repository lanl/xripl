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
      packages=['xripl'],
      zip_safe=False)