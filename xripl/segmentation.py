#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 10:10:36 2019

Image segmentation tools for radiographic images.

@author: Pawel M. Kozlowski
"""

# python modules
import numpy as np
from scipy import ndimage as ndi
from skimage import measure
from skimage.morphology import watershed, disk
from skimage.filters import median, rank
from skimage.filters.rank import maximum, minimum
import matplotlib.pyplot as plt

# custom modules
from xripl.contour import nContours
import xripl.pltDefaults


def merge_labels(labels_image,
                 labels_to_merge,
                 label_after_merge):
    r"""
    Utility function for merging different labeled regions.
    """
    labels_map = np.arange(np.max(labels_image) + 1)
    labels_map[labels_to_merge] = label_after_merge
    return labels_map[labels_image]


def nSegments(labels, n):
    """
    Get the n largest area segments from a segmented (labeled) image.
    
    labels: numpy.ndarray
        A segmented 2D image.
        
    n: int
        Number of segments to select.
    """
    # getting region properties of segments
    props = measure.regionprops(labels)
    # getting areas of segments
    areas = np.array([p['filled_area'] for p in props])
    # getting label number corresponding to each segments
    numbers = np.array([p['label'] for p in props])
    # sorting indices of areas list based on area size of segment
    areasIdxSorted = np.argsort(areas)[::-1]
    # Reducing sorted index list to n largest areas
    largestAreasIdxs = areasIdxSorted[:n]
    # filtering segments list using selected indices of n largest segments
    largestSegments = numbers[largestAreasIdxs]
    return largestSegments


def segmentContour(labels, segmentNumber, plots=False):
    """
    Given a segmented image and a selected segment number, obtains the
    longest contour of that segment.
    
    labels: numpy.ndarray
        A segmented 2D image.
        
    segmentNumber: int
        Which labeled segment to choose for obtaining contour.
    
    plots: bool
        Flag for plotting longest contour over binary image of segment.
    """
    # transforming image into binary based on selected label
    binImg = labels == segmentNumber    
    # Getting contours of segment
    contoursSegment = measure.find_contours(binImg, 0)    
    # selecting the longest contour
    contourLongest = nContours(contoursSegment, 1)[0]
    if plots:
        # and plotting longest contour over binary image
        plt.imshow(binImg)
        plt.plot(contourLongest[:, 1], contourLongest[:, 0], linewidth=2)
        plt.show()
    return contourLongest


#%% collection of methods for detection of shock position in radiographs
    
def detectShock(image,
                originalImage=None,
                medianDisk=40,
                gradientDiskMarkers=10,
                gradientThreshold=10,
                gradientDiskWatershed=4,
                morphDisk=10,
                compactness=0,
                plots=True,
                nSegs=3):
    """
    This is a convenience function for applying watershed segmentation using
    regions of low gradient as markers, and using another gradient image
    for processing via watershed.
    
    Steps:
        1st the image is denoised using a median filter
        2nd the gradient of the image is obtained and thresholded to generate
            markers to be used for watershed segmentation.
        3rd Morphological closing operation is applied to markers to make
            the region boundaries thicker and the marker regions more
            continous.
        4th Another gradient image is generated, which will be processed
            via watershed.
        5th The gradient image in step 4 and the markers from step 3 are
            processed using watershed segmentation.
    
    image: numpy.ndarray
        Image to be processed for shock detection.
        
    originalImage: numpy.ndarray
        Original image, in case user want to plot contours and segments
        over a different image. Default is None.
        
    medianDisk: int
        Size of disk used in median filter application.
        
    gradientDiskMarkers: int
        Size of disk used in gradient function for determining watershed
        markers. This makes the gradient image smoother.
        
    gradientThreshold: int
        Maximum size of gradient to be used for selecting watershed
        markers.
        
    gradientDiskWatershed: int
        Size of disk used in gradient function for generating image to be
        processed by watershed. This makes the gradient image smoother.
        
    morphDisk: int
        Size of disk used in morphological closing of markers image. This
        cleans up the markers into more continuous regions. If zero, then
        this step is skipped.
        
    compactness: float
        Compactness parameter for watershed. 
        See skimage.morphology.watershed().
        
    plots: bool
        Flag for plotting results
        
    nSegs: int
        Obtains contours of the largest segments by filled area.
    """
    if not type(originalImage) == np.ndarray:
        originalImage = image
    # normalizing image and original
#    image_norm = image / np.max(img)
    original_norm = originalImage / np.max(originalImage)
    denoised = median(image, disk(medianDisk))
    # normalizing
    denoised_norm = denoised / np.max(denoised)
    # find continuous region (low gradient - where less than gradientThreshold
    # for this image) --> markers
    # disk(gradientDiskMarkers) is used here to get a more smooth image
    rankGrad = rank.gradient(denoised_norm, disk(gradientDiskMarkers))
    markers = rankGrad < gradientThreshold
    
    # morphological operations on markers to close some gaps that blend
    # the shock with the background
    if morphDisk != 0:
        closing = maximum(minimum(markers, disk(morphDisk)), disk(morphDisk))
    else:
        closing = markers
    
    # plotting morphologically closed markers
    plt.imshow(closing)
    plt.title('Markers - morphologically closed')
    plt.show()
    
    # labeling markers
    markers = ndi.label(closing)[0]
    
    # local gradient (disk() is used to keep edges thin). This gradient is
    # used directly in the watershed.
    gradient2 = rank.gradient(denoised_norm, disk(gradientDiskWatershed))
    
    # process using watershed
    labels = watershed(gradient2, markers, compactness=compactness)
    
    # getting contours for largest area segments
    contoursList = []
    largestSegments = nSegments(labels=labels, n=nSegs)
    for segmentNumber in largestSegments:
        # get longest contour for each segment
        contourLongest = segmentContour(labels=labels,
                                        segmentNumber=segmentNumber,
                                        plots=False)
        # save the contour to list
        contoursList.append(contourLongest)
    
    # plotting results
    if plots:
        # denoised image
        fig, ax = plt.subplots(figsize=(12, 8))
        plt.imshow(denoised_norm)
        plt.colorbar()
        plt.title('Denoised')
        plt.show
        
        # comparisons between original, gradient, markers, and segmented
        # images.
        fig, axes = plt.subplots(nrows=2,
                                 ncols=2,
                                 figsize=(12, 12),
                                 sharex=True,
                                 sharey=True)
        ax = axes.ravel()
        
        ax[0].imshow(original_norm)
        ax[0].set_title("Original")
        
        ax[1].imshow(gradient2, cmap=plt.cm.tab20)
        ax[1].set_title("Local Gradient")
        
        ax[2].imshow(markers, cmap=plt.cm.tab20)
        ax[2].set_title("Markers")
        
        ax[3].imshow(original_norm, cmap=plt.cm.gray)
        ax[3].imshow(labels, cmap=plt.cm.tab20, alpha=.3)
        ax[3].set_title("Segmented")
        fig.tight_layout()
        plt.show()
        
        # Bigger image of segmentation
        fig, ax = plt.subplots(figsize=(12, 8))
        plt.imshow(original_norm, cmap=plt.cm.gray)
        plt.imshow(labels, cmap=plt.cm.tab20, alpha=.5)
        plt.title('Segments')
        plt.tight_layout()
        plt.show()
        
        # plotting contours
        fig, ax = plt.subplots(figsize=(12, 8))
        plt.imshow(original_norm, cmap=plt.cm.gray, vmax=0.3)
        plt.colorbar()
        for contour in contoursList:
            plt.plot(contour[:, 1], contour[:, 0], linewidth=2)
        plt.title('Contours of segments')
        plt.show()
            
        
#        # getting contours
#        contoursList = []
#        vals = np.arange(np.max(labels)) + 1
#        fig, ax = plt.subplots(figsize=(12, 8))
#        plt.imshow(original_norm, cmap=plt.cm.gray)
#        plt.colorbar()
#        for n in vals:
#            contours = measure.find_contours(labels, n)
#            if contours:
#                contour = contours[0]
#                contoursList.append(contour)
#                plt.plot(contour[:, 1], contour[:, 0], linewidth=2)
#        plt.title('Contours of segments')
#        plt.show()
    
    return labels, contoursList, gradient2, markers