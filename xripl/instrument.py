#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 12:58:48 2019

Utilities for convolving 2D radiograph instrument
function with synthetically produced radiographs.

@author: Pawel M. Kozlowski
"""

# python modules
import os
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import skimage
from skimage import filters

# custom modules
import xripl.pltDefaults



#%% functions
def openSyntheticRadiograph(directory, fileName, plot=False):
    """
    Given the full filename (with path) to an hdf5 file containing
    synthetic radiograph data, open the file and return the image data as
    a numpy array.
    
    fileName is a str
    """
    with h5.File(directory + fileName, "r") as f:
        rasterImg = f['Raster Image #0'][...].transpose()
    
    if plot:
        plt.imshow(rasterImg)
        plt.title(fileName)
        plt.show()
    return rasterImg


def saveHdf(data, directory, fileName):
    """
    Saves radiograph into HDF5 file.
    """
    fullName = directory + fileName
    with h5.File(fullName, "w") as f:
        f.create_dataset("Raster Image #1", data=data)
    return


