# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 16:46:08 2018

Functions for adjusting plotting and adjusting the contrast
of radiographic images.

@author: Pawel M. Kozlowski
"""

# python modules
#import numpy as np
import matplotlib.pyplot as plt
from skimage import exposure
#from skimage.morphology import disk, square
#from skimage.filters import rank
    
# custom modules
import xripl.pltDefaults



#%% global and CLAHE contrast equalization

def equalize(image,
             plot=False,
             savePlot=False,
             fileName="",
             saveDir="",
             cmap='viridis',
             kernel_size=(256, 256),
             clip_limit=0.03,
             nbins=256):
    """
    Convenience function for applying contrast equalization to radiographic
    data. Applies both global contrast equalization and CLAHE equalization.
    """
    # globally equalized contrast image
    globalImg = exposure.equalize_hist(image)
    
    # CLAHE equalized contrast image
#    claheImg = exposure.equalize_adapthist(image,
#                                          kernel_size=(256,256),
#                                          clip_limit=0.03,
#                                          nbins=256)
    
    claheImg = exposure.equalize_adapthist(image,
                                           kernel_size=kernel_size,
                                           clip_limit=clip_limit,
                                           nbins=nbins)

    # locally equalized contrast image
    #selem = disk(100)
    ##selem = square(1000)
    #locallyEqualized = rank.equalize(foreground, selem=selem)
    
    if plot:
        plt.figure(figsize=(10,10))
        plt.imshow(image, cmap=cmap)
        plt.title(f"{fileName} Unprocessed image")
        plt.show()
        # plot the contrast equalized images along with histograms
        # plotting globally equalized images
        plt.figure(figsize=(10,10))
        plt.imshow(globalImg, cmap=cmap)
        plt.title(f"{fileName} Globally equalized contrast")
        plt.show()
        
        # ravel to flatten image array and plot histogram of intensity
#        plt.hist(globalImg.ravel(), bins=256)
#        plt.title(f"{fileName} Globally equalized histogram")
#        plt.show()
        
        # plotting CLAHE equalized images
        plt.figure(figsize=(10,10))
        plt.imshow(claheImg, cmap=cmap)
        plt.title(f"{fileName} CLAHE equalized")
        plt.show()
        
        # ravel to flatten image array and plot histogram of intensity
#        plt.hist(claheImg.ravel(), bins=256)
#        plt.title(f"{fileName} CLAHE equalized histogram")
#        plt.show()
        
        # plotting locally equalized images
        #plt.imshow(locallyEqualized)
        #plt.title("Locally Equalized Intensity")
        #plt.show()
        #
        ## ravel to flatten image array and plot histogram of intensity
        #plt.hist(locallyEqualized.ravel(), bins=256)
        #plt.title("Locally Equalized intensity histogram")
        #plt.show()
        
    if savePlot:
        plt.figure(figsize=(10,10))
        plt.imshow(image, cmap=cmap)
        plt.title(f"{fileName} Unprocessed image")
        fname = saveDir + fileName + ".jpg"
        plt.savefig(fname=fname)
        # plot the contrast equalized images along with histograms
        # plotting globally equalized images
        plt.figure(figsize=(10,10))
        plt.imshow(globalImg, cmap=cmap)
        plt.title(f"{fileName} Globally equalized contrast")
        fname = saveDir + fileName + "_global.jpg"
        plt.savefig(fname=fname)
        
        # plotting CLAHE equalized images
        plt.figure(figsize=(10,10))
        plt.imshow(claheImg, cmap=cmap)
        plt.title(f"{fileName} CLAHE equalized")
        fname = saveDir + fileName + "_CLAHE.jpg"
        plt.savefig(fname=fname)
        
    return globalImg, claheImg
