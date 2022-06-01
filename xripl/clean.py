#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 13:13:52 2019

Functions for cleaning and regularizing images.

@author: Pawel M. Kozlowski
"""

# python modules
import numpy as np
from skimage.morphology import disk, opening, closing
from skimage.filters import median, gaussian
import matplotlib.pyplot as plt

# custom modules
import xripl.pltDefaults


def cleanArtifacts(image,
                   diskSize=5,
                   plots=False,
                   vmin=0,
                   vmax=1,
                   flip=False):
    """
    Applies morphological opening to clean bright streaks and spots from
    radiographs, and then applies a morphological closing to remove dark
    artifacts.
    
    image: numpy.ndarray
        Image containing artifacts to be cleaned.
        
    diskSize: int
        Size of disk to be used as convolving element for removing artifcats.
        
    plots: bool
        Flag for displaying plots of processed images.
        
    vmin: float
        Value between 0 and 1 for setting minimum threshold in plotting image.
        See matplotlib.pyplot.imshow().
        
    vmax: float
        Value between 0 and 1 for setting maximum threshold in plotting image.
        See matplotlib.pyplot.imshow().
        
    flip: bool
        Flips order of opening and closing operations. When False, opening
        is applied first, then closing. When True, closing is applied first,
        then opening. False is used by default for radiographs, and True
        is used for inverted radiographs
    """
    if flip:
        imgClosed = closing(image, disk(diskSize))
        cleaned = opening(imgClosed, disk(diskSize))
    else:
        imgOpen = opening(image, disk(diskSize))
        cleaned = closing(imgOpen, disk(diskSize))
    
    if plots:
        fig, axes = plt.subplots(nrows=1,
                                 ncols=3,
                                 figsize=(12, 12),
                                 sharex=True,
                                 sharey=True)
        ax = axes.ravel()
        
        ax[0].imshow(image, vmin=vmin, vmax=vmax)
        ax[0].set_title("Original")
        
        if flip:
            ax[1].imshow(imgClosed)
            ax[1].set_title("Closed")
            
            ax[2].imshow(cleaned)
            ax[2].set_title("Opened")
        else:
            ax[1].imshow(imgOpen)
            ax[1].set_title("Opened")
            
            ax[2].imshow(cleaned)
            ax[2].set_title("Closed")
        
        fig.tight_layout()
        plt.show()
    return cleaned


def flatten(image, medianDisk=100, gaussSize=100, plots=False, vmin=0, vmax=1):
    """
    Produces an approximate image of the background light intensity
    variations in the image and divides the image by this background to
    effectively flatten the contrast.
    
    image: numpy.ndarray
        Image whose background brightness variation is to be removed via
        flattening.
        
    medianDisk: int
        Size of disk used in median filtering to smooth out all structures
        in image other than background light variations.
        
    gaussSize: int
        Size of Gaussian smoothing used on background image produced by
        median filtering. This smooths out ridges that appear in the
        median filtered image.
        
    plots: bool
        Flag for displaying plots of processed images.
    """
    
    # removing background from image
    denoised = median(image, disk(medianDisk))
    # smoothing background
    gaussed = gaussian(denoised, sigma=gaussSize)
    # renaming
    pseudoFlatfield = gaussed
    # applying pseudo flatfield
    flat = image / pseudoFlatfield
    # filtering nan and inf values
    flat[np.isnan(flat)] = 0
    flat[np.isinf(flat)] = 0
    # reshaping from flat array to 2D array after filtering out nan values
    imgShape = np.shape(image)
    flat = flat.reshape(imgShape)
    # normalizing
    flat_norm = flat / np.max(flat)
    
    if plots:
        fig, axes = plt.subplots(nrows=1,
                                 ncols=3,
                                 figsize=(12, 12),
                                 sharex=True,
                                 sharey=True)
        ax = axes.ravel()
        
        ax[0].imshow(image, vmin=vmin, vmax=vmax)
        ax[0].set_title("Original")
        
        ax[1].imshow(pseudoFlatfield, vmin=vmin, vmax=vmax)
        ax[1].set_title("Background")
        
        ax[2].imshow(flat_norm, vmin=vmin, vmax=vmax)
        ax[2].set_title("Flattened")
        
        fig.tight_layout()
        plt.show()
    return flat_norm


def enhanceRadiograph(img,
                      medianDisk=5,
                      morphDisk=5,
                      flattenMedian=100,
                      flattenGauss=100,
                      plots=False):
    r"""
    Median filter, morphological filter, and pseudo-flatfield the
    radiographs to prepare it for feature identification.
    
    img : numpy.ndarray
        Foreground radiographic image as a 2D numpy array, which is
        to be cleaned/enhanced.
        
    medianDisk : int
        Radial size of disk in pixels to be used for median filtering
        the image. Default is radius of 5 pixels.
        
    morphDisk : int
        Radial size of disk in pixels to be used for morphologically
        filtering the image to clean up artifacts.
        
    flattenMedian : int
        Radial size of disk in pixels to be used for median filtering
        image as part of over-smoothing process to obtain the
        pseudo-flatfield. Default is radius of 100 pixels.
        
    flattenGauss : int
        Standard deviation in pixels to be used for Gaussian blurring
        the image as part of over-smoothing process to obtain the
        pseudo-flatfield. Default is sigma of 100 pixels.
        
    plots : bool
        Flag for plotting cleaned and flattened images. Default is False.
    """
    # normalizing image intensity to max value
    img_norm = img / np.max(img)
    # median filtering to denoise the image
    denoised = median(img_norm, disk(medianDisk))
    denoised_norm = denoised / np.max(denoised)
    # removing artifacts (e.g. xrfc streaks, hot pixels, etc.)
    cleaned = cleanArtifacts(image=denoised_norm,
                             diskSize=morphDisk,
                             plots=plots)
    # Flattening image by dividing out approxiamte background
    flattened = flatten(image=cleaned,
                        medianDisk=flattenMedian,
                        gaussSize=flattenGauss,
                        plots=plots)
    
    # returns median filtered image, morphologically filtered image
    # and pseudo-flatfielded image as a tuple.
    return denoised, cleaned, flattened