#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 15:32:34 2019

Opening and processing microD scanned films.

@author: Pawel M. Kozlowski
"""

# python modules
import h5py as h5


#%% functions

def openFilm(fileName):
    """
    Opens HDF5 file film scan from microD.
    """
    with h5.File(fileName, "r") as f:
        stuff = f['pds_image'][...]
    return stuff


