# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 13:14:35 2016

@author: samuel
"""

import numpy as np
import pyfits
#import aplpy
from scipy.signal import convolve2d
#import sys



def makeGaussian(size, fwhmX, fwhmY, center=None):
    x = np.arange(0, size, 1, float)
    y = x[:,np.newaxis]
    
    if center is None:
        x0 = y0 = size // 2
    else:
        x0 = center[0]
        y0 = center[1]
    
    return (1./(2*np.pi*fwhmX*fwhmY))*np.exp((((x-x0)**2)/2*fwhmX**2)+(((y-y0)**2)/2*fwhmY**2))
    

def run_test():	
    #Read fits file
    hdu = pyfits.open('/home/samuel/Downloads/n2541_lr.fits')
    header = hdu[0].header
    data = hdu[0].data
    
    """ #replace all pixels with 0
    data.fill(0)
    
    #Replace pixel (30,40,50) with 1    
    data[50,40,30]=1."""
    
    #fetch content of CDELT1 header variable and make gaussian
    pix_val = abs(header['CDELT1'])
    #fwhmX = 60./(pix_val*3600)
    #fwhmY = 120./(pix_val*3600)
    fwhm = 30./(pix_val*3600)
    map_2d = makeGaussian(size = 5*fwhm, fwhm=fwhm, center=None)
    #map_2d = makeGaussian(size = 5*fwhmY, fwhmX=fwhmX, fwhmY=fwhmY, center=None)
    
    columnCount = len(data[0][0])
    data1 = np.zeros((1,columnCount,columnCount))
    
    for i in range(len(data)):
        conv_map = convolve2d(in1 = data[i], in2 = map_2d, mode = 'same')
        conv_map=conv_map.reshape((1,170,170))
        data1 = np.append(data1, conv_map, axis=0)
    
    data1 = np.delete(data1,0,axis=0)
    pyfits.writeto('/home/samuel/Documents/newFits3.fits',data1,header)

run_test()

