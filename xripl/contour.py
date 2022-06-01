# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 16:47:46 2018

Tools for identifying contours of equal intensity/contrast.

@author: Pawel M. Kozlowski
"""

# python modules
import numpy as np


def nContours(contours, n):
    """
    Get the n longest contours from a list of contours.
    
    contours: list
        A list of contours from skimage.measure.find_contours().
        
    n: int
        Number of contours to select.
    """
    # getting lengths of contours arrays
    contLens = np.array([len(cont) for cont in contours])
    # sorting indices of contour list based on length of contour
    contIdxSorted = np.argsort(contLens)[::-1]
    # Reducing sorted index list to n longest contours
    longestContoursIdxs = contIdxSorted[:n]
    # filtering contour list using selected indices of n longest contours
    contours_np = np.array(contours)
    longestContours = contours_np[longestContoursIdxs]
    return longestContours