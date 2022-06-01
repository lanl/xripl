#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 09:50:47 2020

Custom filters for cleaning/blurring images.

@author: Pawel M. Kozlowski
"""

import numpy as np
from scipy import ndimage

def boxFilter(img, boxSize=2):
    """
    Applies a symmetric box filter to blur the image. A box filter
    approaches a Gaussian filter for large number of filterings, but
    at smaller kernel sizes it causes less blur. Convolution is
    handled using scipy.ndimage.convolve, and edges condition is 'reflect'.
    
    img : numpy.ndarray
        2D numpy array of the image to be filtered.
        
    boxSize : int
        Length in pixels of the side of the box. The box is symmetric.
        Default size 2 pixels by 2 pixels.
        
    filteredImg : numpy.ndarray
        Box filtered image returned as a 2D numpy array.
    """
    boxKernel = np.ones((boxSize, boxSize)) / boxSize ** 2
    filteredImg = ndimage.convolve(img, boxKernel, mode='reflect')
    return filteredImg