# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 16:44:47 2018

Convenience functions for visualizing radiographic data and
processed data from XRIPL.

@author: Pawel M. Kozlowski
"""

# python modules
import numpy as np
import matplotlib.pyplot as plt


def spatialConversion(img, px2Um, pxRef, umRef, method='vertical'):
    r"""
    Generates spatial extents of image in micrometers, by using
    the image shape, pixel to micrometer conversion factor, and
    a reference position defined in both pixel and micrometer
    coordinates.
    
    img : numpy.ndarray
        Image for getting spatial conversion coordinates.
        
    px2Um : float
        Conversion factor micrometers / pixel for the image.
        
    pxRef : tuple
        Reference position in pixels.
        
    umRef : tuple
        Reference position in micrometers.
        
    method : str
        Marble images are horizontal by default, but we make them
        vertical to match Ranjan SBI paper with shock propagating
        downward. Default shock direction is vertical.
    
    """
    shape = np.shape(img)
    if method == 'vertical':
        # getting spatially calibrated axes. This works for cropped
        # image with shock propagating from top to bottom of image.
        hoMin = (0 - pxRef[0]) * px2Um + umRef[1]
        hoMax = (shape[1] - pxRef[0]) * px2Um + umRef[1]
        vertMin = (0 - pxRef[1]) * px2Um + umRef[0]
        vertMax = (shape[0] - pxRef[1]) * px2Um + umRef[0]
        extent = [hoMin, hoMax, vertMax, vertMin]
    elif method == 'horizontal':
        # getting spatially calibrated axes. This works for full,
        # uncropped image in oriented with shock propagating in
        # horizontal direction from right to left.
        hoMin = -1 * ((0 - pxRef[0]) * px2Um - umRef[0])
        hoMax = -1 * ((shape[1] - pxRef[0]) * px2Um - umRef[0])
        vertMin = (0 - pxRef[1]) * px2Um + umRef[1]
        vertMax = (shape[0] - pxRef[1]) * px2Um + umRef[1]
        extent = [hoMin, hoMax, vertMax, vertMin]
    else:
        raise Exception(f"No such method {method}!")
    return extent


def overlayTube(img, extent, method='vertical'):
    r"""
    Overlays known coordinates of tube based on shock tube dimensions
    onto the given image.
    
    img : numpy.ndarray
        Spatially calibrated radiograph.
        
    extent : list
        Extent coordinates for plotting the spatially calibrated image
        using plt.imshow(). See spatialCovnersion().
        
    method : str
        Orientation of image. This should be the same as used
        in spatialConversion() to get extent.
    """
    plt.figure(figsize=(10,12))
    plt.imshow(img, extent=extent)
    if method == 'vertical':
        # inner tube diameter
        plt.axvline(-250, color='red', ls='--')
        plt.axvline(250, color='red', ls='--')
        # outer tube diameter
        plt.axvline(-300, color='red', ls='--')
        plt.axvline(300, color='red', ls='--')
        plt.xlabel(r'Radial ($\rm \mu m$)')
        plt.ylabel(r'Axial ($\rm \mu m$)')
    elif method == 'horizontal':
        # inner tube diameter
        plt.axhline(-250, color='red', ls='--')
        plt.axhline(250, color='red', ls='--')
        # outer tube diameter
        plt.axhline(-300, color='red', ls='--')
        plt.axhline(300, color='red', ls='--')
        plt.xlabel(r'Axial ($\rm \mu m$)')
        plt.ylabel(r'Radial ($\rm \mu m$)')
    else:
        raise Exception(f"No such method {method}!")
    plt.title('Tube coordinates check')
#    plt.axis([1500, 750, -350, 350])
    plt.show()
    return


def cropImgCalibrated(img,
                      px2Um,
                      pxRef,
                      umRef,
                      xMin,
                      xMax,
                      yMin,
                      yMax,
                      method='horizontal',
                      plots=False):
    r"""
    Crops the image and provides updated extents for spatial
    calibration of the image.
    
    img : numpy.ndarray
        Image to be cropped.
        
    px2Um : float
        Conversion factor micrometers / pixel for the image.
        
    pxRef : tuple
        Reference position in pixels for the uncropped image. This
        is based on a known feature, such as a fiducial or filter edge.
        
    umRef : tuple
        Reference position in micrometers. This is the same reference
        used for pxRef, but with the known target coordinates from
        metrology/design.
        
    xMin : int
        Lower bound pixel for cropping in x-direction.
        
    xMax : int
        Upper bound pixel for cropping in x-direction.
        
    yMin : int
        Lower bound pixel for cropping in y-direction.
        
    yMax : int
        Upper bound pixel for cropping in y-direction.
        
    method : str
        Direction of shock propagation in the image. Default shock
        direction is horizontal.
        
    plots : bool
        Flag for plotting cropped image with spatially calibrated axes.
        Default is False.
    """
    # cropping the image
    img_crop = img[yMin:yMax, xMin:xMax]
    
    # transforming coordinates for cropped image
    pxRefCrop = (pxRef[0] - xMin, pxRef[1] - yMin)
    
    # spatial calibration for cropped image
    extent_crop = spatialConversion(img=img_crop,
                                    px2Um=px2Um,
                                    pxRef=pxRefCrop,
                                    umRef=umRef,
                                    method=method)
    
    if plots:
        # plotting the cropped image
        plt.imshow(img_crop, extent=extent_crop)
        #plt.scatter(pxRefCrop[0],
        #            pxRefCrop[1],
        #            marker="+",
        #            c="C6",
        #            s=1000)
        plt.scatter(umRef[0],
                    umRef[1],
                    marker="+",
                    c="C6",
                    s=1000)
        plt.xlabel(r'Axial ($\rm \mu m$)')
        plt.ylabel(r'Radial ($\rm \mu m$)')
        plt.title("Cropped")
        plt.show()
    # returns cropped image, extents for applying spatial calibration
    # when plotting the cropped image, and the updated pixel position
    # of the reference point used for calibration.
    return img_crop, extent_crop, pxRefCrop


def rotateImgCalibrated(img,
                        px2Um,
                        pxRef,
                        umRef,
                        method='vertical',
                        plots=False):
    r"""
    Rotates the image 90 degrees in counter clockwise direction, and
    provides updated extents for spatial calibration of the image.
    
    img : numpy.ndarray
        Image to be rotated.
        
    px2Um : float
        Conversion factor micrometers / pixel for the image.
        
    pxRef : tuple
        Reference position in pixels for the unrotated image. This
        is based on a known feature, such as a fiducial or filter edge.
        
    umRef : tuple
        Reference position in micrometers. This is the same reference
        used for pxRef, but with the known target coordinates from
        metrology/design.
        
    method : str
        Direction of shock propagation in the newly rotated image. Default
        shock direction is vertical.
        
    plots : bool
        Flag for plotting rotated image with spatially calibrated axes.
        Default is False.
    """
    # rotating 90 degrees CCW using a transpose and a flip
    img_rot = np.flipud(img.transpose())
    cropShape = np.shape(img_rot)
    # getting updated px position of reference point for the rotated
    # image.
    pxRefRot = (pxRef[1], cropShape[0] - pxRef[0])
    # getting updated spatially calibrated axes extents for the
    # newly rotated image.
    extent_rot = spatialConversion(img=img_rot,
                                   px2Um=px2Um,
                                   pxRef=pxRefRot,
                                   umRef=umRef,
                                   method=method)
    
    if plots:
        # plotting the rotated image
        plt.imshow(img_rot, extent=extent_rot)
        #plt.scatter(pxRefFlip[0],
        #            pxRefFlip[1],
        #            marker="+",
        #            c="C6",
        #            s=1000)
        plt.scatter(umRef[1],
                    umRef[0],
                    marker="+",
                    c="C6",
                    s=1000)
        plt.xlabel(r'Radial ($\rm \mu m$)')
        plt.ylabel(r'Axial ($\rm \mu m$)')
        plt.title("Rotated")
        plt.show()
    return img_rot, extent_rot, pxRefRot


def lineoutsComparison1(imgRaw,
                        imgDenoised,
                        imgCleaned,
                        px,
                        extent=None,
                        showFlag=True):
    r"""
    Plots normalized lineouts for raw, denoised, and cleaned iamges for
    comparison. Plot shows how well noise is removed and how
    well features are preserved.
    
    imgRaw : numpy.ndarray
        Raw radiographic image.
        
    imgDenoised : numpy.ndarray
        Denoised (median filtered) radiographic image.
        
    imgCleaned : numpy.ndarray
        Cleaned (morphologically filtered) radiographic image.
        
    px : int
        Pixel position at which to take the lineouts.
        
    extent : list
        Extents defining spatial axes. Used to form radial axis in um.
        Default is None, which falls back on radial axis in pixels.
        
    showFlag : bool
        Flag for showing the plotted image. Set to False if you want
        to further modify the plot. Default is True.
    """
    # lineout and normalized lineout from raw image
    lineoutY = imgRaw[px, :]
    lineoutY = lineoutY / np.max(lineoutY)
    # lineout and normalized lineout from denoised (median filtered) iamge.
    lineoutYDenoised = imgDenoised[px, :]
    lineoutYDenoised = lineoutYDenoised / np.max(lineoutYDenoised)
    # lineout and normalized lineout from cleaned (morphologically filtered)
    # image.
    lineoutYCleaned = imgCleaned[px, :]
    lineoutYCleaned = lineoutYCleaned / np.max(lineoutYCleaned)
    # forming x-axis basis of lineouts
    if extent:
        lineoutX = np.linspace(start=extent[0],
                               stop=extent[1],
                               num=np.shape(imgRaw)[1])
    else:
       lineoutX = np.arange(np.shape(imgRaw)[1])
      
    # plotting
    plt.plot(lineoutX, lineoutY, label='orig')
    plt.plot(lineoutX, lineoutYDenoised, label='denoised')
    plt.plot(lineoutX, lineoutYCleaned, label='cleaned')
    if extent:
        plt.xlabel(r'Radial ($\rm \mu m$)')
    else:
        plt.xlabel('Radial (px)')
    plt.legend(frameon=False,
               labelspacing=0.001,
               borderaxespad=0.1)
    
    if showFlag:
        plt.show()
    return    


def lineoutsComparison2(imgDenoised,
                        imgFlat,
                        px,
                        extent=None,
                        showFlag=True):
    r"""
    Compares pseudo-flatfielded lineout against denoised lineout.
    Pseudo-flatfielded lineout typically includes cleaning via
    morphological filtering, which can distort the image, whereas
    denoising is done through median filtering, which typically
    preserves features. This means this comparison is important
    for showing whether features are preserved through the morphological
    filtering step and whether the pseudo-flatifield suitably 
    flattens the intensity curve compared to what we expect.
    In addition, this overlays expected tube positions for Marble
    VC 16A target.
    
    imgDenoised : numpy.ndarray
        Denoised (median filtered) radiographic image.
        
    imgFlat : numpy.ndarray
        Pseudo-flatfielded image (using over-blurring).
        
    px : int
        Pixel position at which to take the lineouts.
        
    extent : list
        Extents defining spatial axes. Used to form radial axis in um.
        Default is None, which falls back on radial axis in pixels.
        
    showFlag : bool
        Flag for showing the plotted image. Set to False if you want
        to further modify the plot. Default is True.
    
    """
    # lineout and normalized lineout from denoised (median filtered) iamge.
    lineoutYRot = imgDenoised[px, :]
    lineoutYRot = lineoutYRot / np.max(lineoutYRot)
    # lineout and normalized lineout from pseudo-flatfielded image.
    lineoutYFlat = imgFlat[px, :]
    lineoutYFlat = lineoutYFlat / np.max(lineoutYFlat)
    # forming x-axis basis of lineouts
    if extent:
        lineoutXFlat = np.linspace(start=extent[0],
                                   stop=extent[1],
                                   num=np.shape(imgFlat)[1])
    else:
       lineoutXFlat = np.arange(np.shape(imgFlat)[1])     
    
    # plotting
    plt.plot(lineoutXFlat, lineoutYFlat, label='flat')
    plt.plot(lineoutXFlat, lineoutYRot, label='denoised')
    plt.axvline(-250, color='red', ls='--')
    plt.axvline(250, color='red', ls='--')
    plt.axvline(-300, color='red', ls='--')
    plt.axvline(300, color='red', ls='--')
    if extent:
        plt.xlabel(r'Radial ($\rm \mu m$)')
    else:
        plt.xlabel('Radial (px)')
    plt.legend(frameon=False,
               labelspacing=0.001,
               borderaxespad=0.1)
    
    if showFlag:
        plt.show()
    return lineoutXFlat, lineoutYFlat