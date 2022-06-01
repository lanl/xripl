#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 10:59:55 2020

Idealized estimate of what a 1D lineout radially through
a cylindrical foam + tube would look like. This is to assist
in correctly identifying which features in a radiograph correspond
to which part of the target for spatial magnification calculation.

@author: Pawel M. Kozlowski
"""
# python modules
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig

# custom modules
import xripl.pltDefaults


def chord(radius, height):
    r"""
    Calculates the horizontal chord length through a circle at a given
    height. If the height is larger than the circle's radius, then
    a chord length of zero is returned.
    
    radius : float
        Radius of the circle. Must be in same units as height.
        
    height : float
        Height along the circle at which to calculate the horizontal
        chord length.
    """
    # taking the absolute value of height in case a negative value is
    # given. Since a circle is symmetric, a negative height coordinate
    # is the same as a positive height coordinate.
    height = np.abs(height)
    if radius <= 0:
        raise Exception(f"Circle radius must be positive.")
    if height > radius:
        return 0
    else:
        return 2 * np.sqrt(radius ** 2 - height ** 2)
    
    
def tubeThickness(innerDiameter,
                  outerDiameter,
                  height):
    r"""
    Calculates the chord lengths through the inner region (foam) and outer
    region (tube wall) for a given target. Here the tube is simply
    an anulus with the given inner and outer diameters as dimensions, and
    the region inside the tube is the "foam" region.
    
    innerDiameter : float
        Inner diameter of the tube, which is also the diameter of the foam.
        
    outerDiameter : float
        Outer diameter of the tube. Must be in same units as innerDiameter
        and height.
        
    height : float
        Height at which to calculate the chord lengths through the
        tube and foam.
    """
    radiusInner = innerDiameter / 2
    radiusOuter = outerDiameter / 2
    # getting chord lengths for the inner and outer circles which
    # describe the tube anulus.
    chordInner = chord(radius=radiusInner, height=height)
    chordOuter = chord(radius=radiusOuter, height=height)
    # thickness of the foam at the given height
    lengthFoam = chordInner
    # thickness of just the tube (excluding the foam) at the given height
    lengthTube = chordOuter - chordInner
    return lengthTube, lengthFoam


def transmission(density, opacity, length):
    r"""
    Calculates the transmission through a uniform material of given
    density, opacity, and length.
    
    density : float
        Mass density of the material in grams per cubic centimeter.
        
    opacity : float
        Opacity of the material (also known as mass attenuation coefficinet)
        in squared centimeters per gram.
        
    length : float
        Attenuation length through the material in centimeters.
    """
    return np.exp(-density * opacity * length)


def tubeTransmission(innerDiameter,
                     outerDiameter,
                     densityTube,
                     densityFoam,
                     opacityTube,
                     opacityFoam,
                     height):
    r"""
    Calculates the transmission through a tube with foam at a given
    height (radial coordinate) through the tube.
    
    innerDiameter : float
        Inner diameter of the tube, which is also the diameter of the foam.
        In units of centimeters.
        
    outerDiameter : float
        Outer diameter of the tube. In units of centimeters.
        
    densityTube : float
        Mass density of the tube material in grams per cubic centimeter.
        
    densityFoam : float
        Mass density of the foam material in grams per cubic centimeter.
        
    opacityTube : float
        Opacity of the tube material (aka mass attenuation coefficient)
        in squared centimeters per gram.
        
    opacityFoam : float
        Opacity of the foam material (aka mass attenuation coefficient)
        in squared centimeters per gram.
        
    height : float
        Height at which to calculate the chord lengths through the
        tube and foam. In units of centimeters.
    """
    # get thickness of tube wall and foam respectively for the given
    # height. These are chord lengths through an anulus.
    lengthTube, lengthFoam = tubeThickness(innerDiameter=innerDiameter,
                                           outerDiameter=outerDiameter,
                                           height=height)
    # transmission through tube
    transTube = transmission(density=densityTube,
                             opacity=opacityTube,
                             length=lengthTube)
    # transmission through foam
    transFoam = transmission(density=densityFoam,
                             opacity=opacityFoam,
                             length=lengthFoam)
    # total transmission is just the multiplication of the two
    # transmissions.
    transTotal = transTube * transFoam
    return transTotal


def plotTubeTransmission(innerDiameter,
                         outerDiameter,
                         densityTube,
                         densityFoam,
                         opacityTube,
                         opacityFoam,
                         heightsArr,
                         plots=True):
    r"""
    Generates a plot transmission versus radial coordinate through
    a tube.
    
    innerDiameter : float
        Inner diameter of the tube, which is also the diameter of the foam.
        In units of centimeters.
        
    outerDiameter : float
        Outer diameter of the tube. In units of centimeters.
        
    densityTube : float
        Mass density of the tube material in grams per cubic centimeter.
        
    densityFoam : float
        Mass density of the foam material in grams per cubic centimeter.
        
    opacityTube : float
        Opacity of the tube material (aka mass attenuation coefficient)
        in squared centimeters per gram.
        
    opacityFoam : float
        Opacity of the foam material (aka mass attenuation coefficient)
        in squared centimeters per gram.
        
    heightsArr : numpy.ndarray
        Array of heights along the tube radial axis at which to calculate the
        chord lengths through the tube and foam for getting transmission.
        These can be negative and positive. In units of centimeters.
        
    plots : bool
        Flag for generating plots. Default is True.
    """
    innerRadius = innerDiameter / 2
    outerRadius = outerDiameter / 2
    # array for storing transmissions. Default value is 1, for no
    # attenuation through the target.
    transmissions = np.ones_like(heightsArr)
    for idx, height in enumerate(heightsArr):
        transmissions[idx] = tubeTransmission(innerDiameter=innerDiameter,
                                              outerDiameter=outerDiameter,
                                              densityTube=densityTube,
                                              densityFoam=densityFoam,
                                              opacityTube=opacityTube,
                                              opacityFoam=opacityFoam,
                                              height=height)
    
    # normalizing heights to inner radius of tube
    heightsArrNormInner = heightsArr / innerRadius
    # normalizing heights to outer radius of tube
    heightsArrNormOuter = heightsArr / outerRadius
    
    if plots:
        # transmission vs height plot
        plt.plot(heightsArr, transmissions)
        plt.axvline(innerRadius, color='red', ls='--')
        plt.axvline(outerRadius, color='red', ls='--')
        plt.xlabel('Radial height (cm)')
        plt.ylabel('Transmission')
        plt.show()
        
        # transmission vs normalized height plot (inner radius)
        plt.plot(heightsArrNormInner, transmissions)
        plt.axvline(1, color='red', ls='--')
        plt.xlabel('Height norm inner')
        plt.ylabel('Transmission')
        plt.show()
        
        # transmission vs normalized height plot (outer radius)
        plt.plot(heightsArrNormOuter, transmissions)
        plt.axvline(1, color='red', ls='--')
        plt.xlabel('Height norm outer')
        plt.ylabel('Transmission')
        plt.show()
    return heightsArr, transmissions, heightsArrNormInner, heightsArrNormOuter


def gaussianBlur(heightsArr,
                 transmissions,
                 stdDevCm,
                 innerDiameter,
                 outerDiameter,
                 plots=False):
    r"""
    
    heightsArr : numpy.ndarray
        Array of heights along the tube radial axis at which chord lengths
        through the tube and foam were used for getting transmission.
        These can be negative and positive. In units of centimeters.
        See plotTubeTransmission().
        
    transmissions : numpy.ndarray
        Transmission values through the tube corresponding to heightsArr.
        See plotTubeTransmission().
        
    stdDevCm : float
        Standard deviation of Gaussian (in centimeters) to be used
        for blurring the transmissions curve.
        
    innerDiameter : float
        Inner diameter of the tube, which is also the diameter of the foam.
        In units of centimeters. Used to overlay tube location on plots.
        
    outerDiameter : float
        Outer diameter of the tube. In units of centimeters. Used to
        overaly tube location on plots.
        
    plots : bool
        Flag for plotting Gaussian used in convolution and blurred
        transmissions curve.
    """
    # Get length of input array to form Gaussian
    lengthArr = len(heightsArr)
    # convert stdDev from cm to pixels
    stdDevPx = int(stdDevCm * (lengthArr / np.max(heightsArr)))
    # normalization factor to make integral of Gaussian equal to 1
    normFactor = 1 / (stdDevPx * np.sqrt(2 * np.pi))
    # forming Gaussian curve
    gaussian = normFactor * sig.gaussian(lengthArr, std=stdDevPx) 
    
    # Padding array edges to avoid edge effects due to convolution.
    # This pads the array with edge values instead of zeros.
    transmissionsPad = np.pad(transmissions,
                              (lengthArr, lengthArr),
                              'edge')
    
    # convolving gaussian with transmission array
    transmissionsBlurPad = sig.convolve(transmissionsPad, 
                                        gaussian,
                                        mode='same')
    
    # removing padded regions to bring length of array back to
    # original length
    transmissionsBlur = transmissionsBlurPad[lengthArr:-lengthArr]
    
    
    if plots:
        # plotting the Gaussian
        plt.plot(heightsArr - np.max(heightsArr)/2, gaussian)
        plt.xlabel('Radial (cm)')
        plt.title('Gaussian for blurring')
        plt.show()
        
        # plotting blurred transmission
        plt.plot(heightsArr, transmissionsBlur)
        # overlaying tube edge locations
        plt.axvline(innerDiameter/2, color='red', ls='--')
        plt.axvline(outerDiameter/2, color='red', ls='--')
        plt.xlabel('Radial height (cm)')
        plt.ylabel('Transmission Blurred')
        plt.ylim(0.55, 1.05)
        plt.show()
    
    return transmissionsBlur


