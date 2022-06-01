#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 14:51:45 2020

@author: Pawel M. Kozlowski
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig

import xripl.pltDefaults
from xripl.reader import shotRadiograph
from xripl.clean import enhanceRadiograph
from xripl.visualizations import cropImgCalibrated, rotateImgCalibrated


def lineoutMinima(lineoutX,
                  lineoutY,
                  window_length=51,
                  polyOrder=3,
                  peakWidth=50,
                  plotsFlag=False):
    r"""
    Given lineout should be lineout from flattened radiograph
    image. This function smoothes the lineout using a Savitzky-Golay
    filter, and finds the 2 deepest minima in the lineout. These minima
    should correspond to the inner diameter edge of the target tube.
    
    lineoutX : numpy.ndarray
        1D array of x-axis points of the lineout from which we
        want to get minima.
        
    lineoutY : numpy.ndarray
        1D array of y-axis points of the lineout from which we want to
        get minima. This should be a radial lineout through the tube target.
        Finds minima in intensity, which should correpsond
        to the inner diameter edge of the tube.
    
    window_length : int
        Window length for Savitzky-Golay filter. Must be odd numbered.
        Default is window that is 51 points long.
    
    polyOrder : int
        Polynomial order for Savitzky-Golay filter. Default is 3 (cubic).
        
    peakWidth : int
        Minimum number of points required in peak width to select
        the peak as a minima. Default is 50 pts wide.
        
    plotsFlag : bool
        Flag for plotting smoothed lineout over input lineout. Also
        plots minima points over smoothed lineout. Default is False.
    """
    # Savitzky-Golay smoothing the signal to prevent noise from
    # distorting peak finder from finding minima corresponding to
    # inner edge of target tube.
    lineoutSmoothed = sig.savgol_filter(lineoutY,
                                        window_length,
                                        polyOrder)
    
    # Inverting the lineout so that peak finder gets minima, since
    # peak finder is made to look for maxima.
    inverted = -lineoutSmoothed
    # Finding peaks with minimum width of peakWidth
    peaks, properties = sig.find_peaks(inverted,
                                       width=peakWidth)
    
    if len(peaks) < 2:
        print("Found fewer than 2 peaks. Trying with smaller width.")
        widthMod = int(peakWidth * 1/2)
        print(f"Trying width of {widthMod} in lieu of {peakWidth}.")
        peaks, properties = sig.find_peaks(inverted,
                                           width=widthMod)
        # setting plot to true for inspection
        plotsFlag = True
    
    # fetching x and y coordinates of peaks
    minimaPeaksX = lineoutX[peaks]
    minimaPeaksY = lineoutSmoothed[peaks]
    
    # filtering list of found peaks to the 2 smallest ones in terms of
    # intensity.
    sortIdxs = np.argsort(minimaPeaksY)
    selectIdxs = sortIdxs[:2]
    minimaPeaksXFilt = minimaPeaksX[selectIdxs]
    minimaPeaksYFilt = minimaPeaksY[selectIdxs]
    
    # getting pixel positions of minima
    minimaIdxs = peaks[selectIdxs]
    
    if plotsFlag:
        # plotting the input lineout against the smoothed lineout to
        # ensure that features were preserved and not over-smoothed
        plt.plot(lineoutX, lineoutY, label='flat')
        plt.plot(lineoutX, lineoutSmoothed, label='smoothed')
        plt.xlabel(r'Radial ($\rm \mu m$)')
        plt.legend(frameon=False,
                   labelspacing=0.001,
                   borderaxespad=0.1)
        plt.show()
        
        # plotting 2 smallest minima over smoothed lineout.
        plt.plot(lineoutX, lineoutSmoothed)
        plt.scatter(minimaPeaksXFilt,
                    minimaPeaksYFilt,
                    c='red',
                    marker='o',
                    s=200)
        plt.xlabel(r'Radial ($\rm \mu m$)')
        plt.show()
    return minimaIdxs, minimaPeaksXFilt, minimaPeaksYFilt


def tubeCenterPx(minimaIdxs, lineoutY=None, plotsFlag=False):
    r"""
    Given the pixel positions of the tube edges, obtains the tube center
    in pixels for a tube target.
    
    minimaIdxs : tuple
        A tuple of ints corresponding to the pixel positions of the
        two minima in intensity found in the radiograph by lineoutMinima().
        These minima correspond to the inner edge of the target tube.
    
    lineoutY : numpy.ndarray
        Intensity values of the lineout from which tube edges were found.
        This is only used for plotting. Default is None.
    
    plotsFlag : bool
        Plots the lineout and overlays the pixel position of the tube edges
        and center. Default is False.
    """
    # checking that two minima were passed
    if np.shape(minimaIdxs) == (2,):
        # finding the lower and higher pixel values
        idxLower = np.min(minimaIdxs) 
        idxUpper = np.max(minimaIdxs)
        center = (idxUpper + idxLower) / 2
    else:
        raise Exception (f"Expected 2 minima, but got {len(minimaIdxs)}!")
        
    # forming x-axis in pixels for plot
    lineoutXPxs = np.arange(len(lineoutY))
    
    # plotting
    if plotsFlag:
        plt.plot(lineoutXPxs, lineoutY)
        plt.axvline(idxLower, color='red', ls='--')
        plt.axvline(idxUpper, color='red', ls='--')
        plt.axvline(center, color='red', ls='--')
        plt.xlabel("Radial (px)")
        plt.ylabel('Intensity (arb.)')
        plt.show()
    return center


def diameterPx(minimaIdxs):
    r"""
    Obtains the diameter of the tube in pixels when given the tube
    edges. Tube edges are obtained using lineoutMinima().
    
    minimaIdxs : tuple
        A tuple of ints corresponding to the pixel positions of the
        two minima in intensity found in the radiograph by lineoutMinima().
        These minima correspond to the inner edge of the target tube.
    """
    # checking that two minima were passed
    if np.shape(minimaIdxs) == (2,):
        # finding the lower and higher pixel values
        idxLower = np.min(minimaIdxs) 
        idxUpper = np.max(minimaIdxs)
    else:
        raise Exception (f"Expected 2 minima, but got {len(minimaIdxs)}!")
    # getting the tube diameter in pixels
    innerDiameterPx = idxUpper - idxLower
    return innerDiameterPx


def magnificationUmPx(innerDiameterPx,
                      stdDevPx=0,
                      innerDiameterUm=500,
                      innerDiameterErrUm=0,
                      printFlag=False):
    r"""
    Get magnification with propagated uncertainty in um/px when given
    target tube diameter in um, in px, and standard deviation on the
    diameter in px.
    
    innerDiameterPx : float
        Measured inner diameter of the target tube in pixels.
        
    stdDevPx : float
        Standard deviation on the inner diameter in pixels. Default is
        zero, for no uncertainty.
    
    innerDiameterUm : float
        Known inner diameter of the target tube in micrometers.
        Default is set to 500 um, which was the nominal diameter for a Marble
        VC target.
        
    innerDiameterErrUm : float
        The error/uncertainty (one sigma) on the inner dimaeter of the
        target tube in micrometers. Default is 0 um.
        
    printFlag : bool
        Flag for printing the calculated magnification. Default is False.
    """
     # getting the magnification (um/px)
    umPerPx = innerDiameterUm / innerDiameterPx
    # error terms for uncertainty propagation based on partial derivatives
    umErrTerm = (innerDiameterPx ** -1) ** 2 * (innerDiameterErrUm) ** 2
    pxErrTerm = (umPerPx / innerDiameterPx) ** 2 * (stdDevPx) ** 2
    # uncertainty on magnification (um/px)
#    stdDevUmPx = np.abs(stdDevPx * umPerPx / innerDiameterPx)
    stdDevUmPx = np.sqrt(umErrTerm + pxErrTerm)
    # printing the magnification, if requested by user
    if printFlag:
        print(f"Magnification is {umPerPx:.3f} +/- {stdDevUmPx:.3f} um/px")
    return umPerPx, stdDevUmPx


#%% BIG BAD MAGNIFICATION ANALYSIS FUNCTION

def magnificationAnalysis(shot,
                          camera,
                          dataDir,
                          px2Um,
                          pxRef,
                          umRef,
                          xMin,
                          xMax,
                          yMin,
                          yMax,
                          cropDownstream=(1000, 1400),
                          innerDiameterUm=500,
                          innerDiameterErrUm=0,
                          saveDir=''):
    r"""
    Get magnification from target radiograph by measuring
    inner tube wall of known diameter.
    
    shot : int
        Shot number to read raw radiographic iamge data from.
        
    camera : str
        Framing camera for which radiographic image to read.
        
    dataDir : str
        Path where data for shot day is stored.
        
    px2Um : float
        Dummy value for magnification conversion to pass to
        initial image loading functions. This just sets the
        axes for those functions.
        
    pxRef : tuple
        Reference position in pixels. This can be a dummy value as
        it is only used by functions loading the image data.
        
    umRef : tuple
        Reference position in micrometers. This can be a dummy value
        as it is only used by functions loading the image data.
        
    xMin : int
        Lower bound pixel for cropping in x-direction.
        
    xMax : int
        Upper bound pixel for cropping in x-direction.
        
    yMin : int
        Lower bound pixel for cropping in y-direction.
        
    yMax : int
        Upper bound pixel for cropping in y-direction.
    
    cropDownstream : tuple
        Tuple of values defining the axial pixel bounds of the downstream
        end of the tube. This is where the tube diameter measurement
        in pixels will be taken. Default is (1000, 1400).
        
    innerDiameterUm : float
        The measured inner diameter of the target tube in
        micrometers. This is used the obtain the magnification in um/px.
        The default is 500 um, which is the nominal value of the Marble VC
        tube.
        
    innerDiameterErrUm : float
        The error/uncertainty (one sigma) on the inner dimaeter of the
        target tube in micrometers. This is used to get the uncertainty
        on the magnification. Default is 0 um.
        
    saveDir : str
        Directory for saving images and data. Default is empty string,
        which does not save the data.
        
    """
    # generating base name for saving iamges and data
    saveStr = saveDir + f'{shot}-{camera}-'
    
    # reading raw image
    imgRaw, _ = shotRadiograph(shotNum=shot,
                               camera=camera,
                               dataDir=dataDir,
                               plots=False)
    
    # crop the image and obtain transforms on spatially calibrated axes
    img_crop, extent_crop, pxRefCrop = cropImgCalibrated(img=imgRaw,
                                                         px2Um=px2Um,
                                                         pxRef=pxRef,
                                                         umRef=umRef,
                                                         xMin=xMin,
                                                         xMax=xMax,
                                                         yMin=yMin,
                                                         yMax=yMax,
                                                         method='horizontal',
                                                         plots=False)
    
    # rotate image to be consistent with Ranjan SBI diagram with shock 
    # propagating downward.
    img_rot, extent_rot, pxRefRot = rotateImgCalibrated(img=img_crop,
                                                        px2Um=px2Um,
                                                        pxRef=pxRefCrop,
                                                        umRef=umRef,
                                                        method='vertical',
                                                        plots=False)
    
    
    # median filtering, morphological filtering, and pseudo-flatfielding
    denoised, cleaned, flattened = enhanceRadiograph(img=img_rot,
                                                     medianDisk=5,
                                                     morphDisk=5,
                                                     flattenMedian=100,
                                                     flattenGauss=100,
                                                     plots=False)
    
    # Selecting downstream region to be used for tube diameter measurement.
    # No need to crop.
    lineoutIdxs = np.arange(start=cropDownstream[0],
                            stop=cropDownstream[1],
                            step=1)
    
    # plotting flatfielded image and downstream region to be used for
    # measuring tube size in pixels
    plt.figure(figsize=(10,12))
    plt.imshow(flattened)
    plt.axhline(cropDownstream[0], color='red', ls='--')
    plt.axhline(cropDownstream[1], color='red', ls='--')
    if saveDir:
        plt.savefig(saveStr + 'flat.png',
                    dpi=300,
                    bbox_inches='tight',
                    pad_inches=0)
    plt.show()
    
    # number of lineouts
    lineoutsNum = cropDownstream[1] - cropDownstream[0]
    
    # initializing arrays for storing tube edges in pixels
    lowerIdxs = np.zeros(lineoutsNum, dtype=int)
    upperIdxs = np.zeros(lineoutsNum, dtype=int)
    centerIdxs = np.zeros(lineoutsNum, dtype=float)
    minimaArr = np.zeros(lineoutsNum, dtype=object)
    
    # produce x-axis array, as this radial axis should be shared by all
    # lineouts in the loop.
    lineoutXFlat = np.arange(np.shape(flattened)[1])
    
    # produce an averaged lineout. This isn't used in the analysis,
    # but is returned to the user for enabling comparisons.
    allLineouts = np.array([flattened[idx, :] for idx in lineoutIdxs])
    lineoutAvg = np.mean(allLineouts, axis=0)
    
    # looping over lineouts
    for idx, lineoutIdx in enumerate(lineoutIdxs):
        # taking lineout through flattened image
        lineoutYFlat = flattened[lineoutIdx, :]
        # finding tube edges. If lineoutX is in units of pixels, then
        # the returned values minimaIdxs and minimaX should be identical.
        minimaIdxs, minimaX, minimaY = lineoutMinima(lineoutX=lineoutXFlat,
                                                     lineoutY=lineoutYFlat,
                                                     window_length=51,
                                                     polyOrder=3,
                                                     peakWidth=40,
                                                     plotsFlag=False)
        # shifting coordinates from being with respect to origin of the
        # cropped image to being with respect to the uncropped image.
        # We shift by yMin, because the image was cropped and then rotated
        # prior to locating tube edges.
        minimaIdxs = minimaIdxs + yMin
        
        # checking that two minima were passed
        if np.shape(minimaIdxs) == (2,):
            # finding the lower and higher pixel values
            idxLower = np.min(minimaIdxs) 
            idxUpper = np.max(minimaIdxs)
        else:
            raise Exception (f"Expected 2 minima, but got {len(minimaIdxs)}!")
        # Finding center pixel position
        centerPx = tubeCenterPx(minimaIdxs=minimaIdxs,
                                lineoutY=lineoutYFlat,
                                plotsFlag=False)
        # recording tube edges and center to arrays for storage
        lowerIdxs[idx] = idxLower
        upperIdxs[idx] = idxUpper
        centerIdxs[idx] = centerPx
        minimaArr[idx] = minimaIdxs
    
    # checking mean, median, and std dev of the wall
    lowerIdxMean = np.mean(lowerIdxs)
    lowerIdxMedian = np.median(lowerIdxs)
    lowerIdxStdDev = np.std(lowerIdxs)
    
    print(f"Lower Wall Mean: {lowerIdxMean:.3f} pixels")
    print(f"Lower Wall Median: {lowerIdxMedian:.3f} pixels")
    print(f"Lower Wall Std. Dev.: {lowerIdxStdDev:.3f} pixels")
    
    # plotting a histogram of the lower wall pixel position
    nLwr, binsLwr, patchesLwr = plt.hist(lowerIdxs,
                                         bins=20)
    plt.axvline(lowerIdxMean, color='red', ls='--')
    plt.axvline(lowerIdxMean - lowerIdxStdDev, color='red', ls='--')
    plt.axvline(lowerIdxMean + lowerIdxStdDev, color='red', ls='--')
    plt.ylabel("# of pts")
    plt.xlabel("Lower wall position (px)")
    if saveDir:
        plt.savefig(saveStr + 'hist-lower-positions.png',
                    dpi=300,
                    bbox_inches='tight',
                    pad_inches=0)
    plt.show()
    
    upperIdxMean = np.mean(upperIdxs)
    upperIdxMedian = np.median(upperIdxs)
    upperIdxStdDev = np.std(upperIdxs)
    
    print(f"Upper Wall Mean: {upperIdxMean:.3f} pixels")
    print(f"Upper Wall Median: {upperIdxMedian:.3f} pixels")
    print(f"Upper Wall Std. Dev.: {upperIdxStdDev:.3f} pixels")
    
    # plotting a histogram of the upper wall pixel position
    nUpr, binsUpr, patchesUpr = plt.hist(upperIdxs,
                                         bins=20)
    plt.axvline(upperIdxMean, color='red', ls='--')
    plt.axvline(upperIdxMean - upperIdxStdDev, color='red', ls='--')
    plt.axvline(upperIdxMean + upperIdxStdDev, color='red', ls='--')
    plt.ylabel("# of pts")
    plt.xlabel("Upper wall position (px)")
    if saveDir:
        plt.savefig(saveStr + 'hist-upper-positions.png',
                    dpi=300,
                    bbox_inches='tight',
                    pad_inches=0)
    plt.show()
    
    # getting tube diameter in pixels for each lineout
    innerDiameterPx = [diameterPx(minimaIdxs) for minimaIdxs in minimaArr]
        
    # Getting mean, median, and standard deviation of tube diameter in pixels
    # for the selected crop region.
    innerDiameterPxMean = np.mean(innerDiameterPx)
    innerDiameterPxMedian = np.median(innerDiameterPx)
    innerDiameterPxStdDev = np.std(innerDiameterPx)
    
    # propagated mean diameter and standard deviation from mean lower
    # and upper Idxs (of tube walls) for comparison
    innerDiameterPxMeanWalls = upperIdxMean - lowerIdxMean
    innerDiameterPxMeansWallErr = np.sqrt(upperIdxStdDev ** 2 + lowerIdxStdDev ** 2)
    
    print(f"Diameter Mean: {innerDiameterPxMean:.3f} pixels")
    print(f"Diameter Median: {innerDiameterPxMedian:.3f} pixels")
    print(f"Diameter Std. Dev.: {innerDiameterPxStdDev:.3f} pixels")
    print(f"Min Diameter in list: {np.min(innerDiameterPx):.3f} pixels")
    print(f"Max Diameter in list: {np.max(innerDiameterPx):.3f} pixels")
    print(f"Diameter propagated from mean edges: {innerDiameterPxMeanWalls:.3f} pixels")
    print(f"Propagated error on diameter from mean edges: {innerDiameterPxMeansWallErr:.3f} pixels")
    
    # plotting a histogram of the measured diameters in pixels
    n, bins, patches = plt.hist(innerDiameterPx,
                                bins=40)
    plt.axvline(innerDiameterPxMean, color='red', ls='--')
    plt.axvline(innerDiameterPxMean - innerDiameterPxStdDev, color='red', ls='--')
    plt.axvline(innerDiameterPxMean + innerDiameterPxStdDev, color='red', ls='--')
    plt.ylabel("# of pts")
    plt.xlabel("Diameter (px)")
    if saveDir:
        plt.savefig(saveStr + 'hist-diameters.png',
                    dpi=300,
                    bbox_inches='tight',
                    pad_inches=0)
    plt.show()
        
    # getting magnification (um/px) and its standard deviation
    umPerPx, stdDevUmPx = magnificationUmPx(innerDiameterPx=innerDiameterPxMean,
                                            stdDevPx=innerDiameterPxStdDev,
                                            innerDiameterUm=innerDiameterUm,
                                            innerDiameterErrUm=innerDiameterErrUm,
                                            printFlag=False)
    print(f"Magnification: {umPerPx:.3f} +/- {stdDevUmPx:.3f} um/px")
    
    # getting mean position of tube center with error
    centerPxMean = np.mean(centerIdxs)
    centerPxMedian = np.median(centerIdxs)
    centerPxStdDev = np.std(centerIdxs)
    
    # propagating center of tube from mean edges of tube for comparison
    centerPxMeanWalls = (upperIdxMean + lowerIdxMean) / 2
    centerPxMeanWallsErr = 0.5 * np.sqrt(upperIdxStdDev ** 2 + lowerIdxStdDev ** 2)
    
    print(f"Center Mean: {centerPxMean:.3f} pixels")
    print(f"Center Median: {centerPxMedian:.3f} pixels")
    print(f"Center Std. Dev.: {centerPxStdDev:.3f} pixels")
    print(f"Center propagated from mean edges: {centerPxMeanWalls:.3f} pixels")
    print(f"Propagated error on center from mean edges: {centerPxMeanWallsErr:.3f} pixels")
        
    # plotting tube edges and center to see if there is any systematic
    # pattern or if variations in position are randomly distributed.
    plt.scatter(lowerIdxs, lineoutIdxs)
    plt.scatter(upperIdxs, lineoutIdxs)
    plt.scatter(centerIdxs, lineoutIdxs)
    # center line with error bounds
    plt.axvline(centerPxMean, color='red', ls='--')
    plt.axvline(centerPxMean + centerPxStdDev, color='red', ls='-')
    plt.axvline(centerPxMean - centerPxStdDev, color='red', ls='-')
    # right wall with error bounds
    plt.axvline(centerPxMean + innerDiameterPxMean/2, color='red', ls='--')
    plt.axvline(upperIdxMean - upperIdxStdDev, color='red', ls='-')
    plt.axvline(upperIdxMean + upperIdxStdDev, color='red', ls='-')
    # left wall with error bounds
    plt.axvline(centerPxMean - innerDiameterPxMean/2, color='red', ls='--')
    plt.axvline(lowerIdxMean - lowerIdxStdDev, color='red', ls='-')
    plt.axvline(lowerIdxMean + lowerIdxStdDev, color='red', ls='-')
    plt.xlabel("Radial (px)")
    plt.ylabel("Axial (px)")
    
    
    # producing a radial coordinate array for the averaged lineout
    lineoutRadii = umPerPx * (lineoutXFlat + yMin - centerPxMean)
    
    if saveDir:
        plt.savefig(saveStr + 'tube-positions.png',
                    dpi=300,
                    bbox_inches='tight',
                    pad_inches=0)
    plt.show()
        
    # saving analysis to dict
    results = {'umPerPx' : umPerPx,
               'stdDevUmPx' : stdDevUmPx,
               'centerPxMean' : centerPxMean,
               'centerPxStdDev' : centerPxStdDev,
               'centerPxMeanWalls' : centerPxMeanWalls,
               'centerPxMeanWallsErr' : centerPxMeanWallsErr,
               'lowerIdxs': lowerIdxs,
               'upperIdxs' : upperIdxs,
               'centerIdxs' : centerIdxs,
               'lineoutIdxs' : lineoutIdxs,
               'innerDiameterPxMean' : innerDiameterPxMean,
               'innerDiameterPxStdDev' : innerDiameterPxStdDev,
               'innerDiameterPxMeanWalls' : innerDiameterPxMeanWalls,
               'innerDiameterPxMeansWallErr' : innerDiameterPxMeansWallErr,
               'lineoutAvg' : lineoutAvg,
               'lineoutRadii' : lineoutRadii}
    
    # returning important values
    return results