# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 16:42:16 2018

Reads radiographic images and create simple plots

@author: Pawel M. Kozlowski
"""

# python modules
import glob
import os
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt

# custom modules
import xripl.pltDefaults


def openRadiograph(fileName):
    """
    Given the full filename (with path) to an hdf5 file containing
    radiographic data from an XRFC (x-ray framing camera) diagnostic
    on OMEGA, open the file and return the foreground and background
    image data as numpy arrays.
    
    fileName is a str
    """
    with h5.File(fileName, "r") as f:
        streakArr = f["Streak_array"][...]
    
    foreground = streakArr[0, :, :]
    background = streakArr[1, :, :]
    return foreground, background


def omegaDataSearch(dataDir, camera='xrfc4'):
    """
    Search given directory and subdirectories for HDF5 files of
    radiographs from OMEGA LLE XRFC data.
    """
    if not camera in ['xrfc1', 'xrfc2', 'xrfc3', 'xrfc4', 'xrfc5']:
        raise Exception(f"Cannot find method for camera {camera}")
        
    # fetch all xrfccd hdf5 files in directory and subdirectories
    pattern = f'**/xrfccd_{camera}*.h5'
    flist = glob.glob(os.path.join(dataDir, pattern), recursive=True)
    # trim the filenames to just base filename
    flistBase = [os.path.basename(fname) for fname in flist]
    # split filename and extension
    flistTrim = [os.path.splitext(fname)[0] for fname in flistBase]
    # extracting shot numbers from file names
    shotNos = [int(fname.split("_")[-1]) for fname in flistTrim]
    # get diagnostic names from prepended portion of filenames
    diagnosticNamesList = ["_".join(fname.split("_")[:-1]) for fname in flistTrim]
    diagnosticNames = set(diagnosticNamesList)
    return flist, shotNos, diagnosticNames, flistTrim


def shotRadiograph(shotNum, camera, dataDir, plots=False):
    r"""
    Opens a radiograph given a shot number, framing camera and
    directory containing shot data.
    
    shotNum : int
        Omega shot number of radiograph to be opened.
        
    camera : str
        Name of camera used on shotNum from which to open radiograph.
        For example, 'xrfc3' for x-ray framing camera 3.
        
    dataDir : str
        Full path to directory containing shot data with radiographs.
        
    plots : bool
        Flag for plotting the background and the foreground images.
        Default is False.
    """
    # get files in directory and pick a shot
    flist, shotNos, diagnosticNames, flistTrim = omegaDataSearch(dataDir=dataDir,
                                                                  camera=camera)
    
    # picking a shot
    if not shotNum in shotNos:
        raise Exception(f"Shot number {shotNum} not found in directory!")
    # looking for shot number in files in directory
    filteredFiles = np.array([str(shotNum) in fileName for fileName in flist])
    # picking just the first match (don't care which diagnostic it is, so long
    # as shot number is correct, since we already filtered based on 
    # camera diagnostic)
    flistArr = np.array(flist)
    xrfcFull = flistArr[filteredFiles][0]
#    baseName = os.path.basename(xrfcFull)
    
    # open the selected radiograph if it is in the list of supported
    # camera types for this data set
    if camera in ['xrfc1', 'xrfc2', 'xrfc3', 'xrfc4', 'xrfc5']:
        foreground, background = openRadiograph(fileName=xrfcFull)
    else:
        raise NotImplementedError(f"Unsupported camera type {camera}.")
    
    if camera == 'xrfc5':
        # mirroring the image so that it is oriented in same direction
        # as XRFC3
        foreground = np.fliplr(foreground)
        background = np.fliplr(background)
    
    if plots:
        plt.imshow(background)
        plt.title(f"Background")
        plt.show()
        
        plt.figure(figsize=(10,12))
        plt.imshow(foreground)
        plt.title(f"Foreground")
        plt.show()
    return foreground, background