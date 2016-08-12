import pyfits
import numpy as np

data, header = pyfits.getdata('/home/samuel/software/samtirifik-master/chapter_01_concepts/01_data/n2541_lr_in.fits',header=True)
pix_val = abs(header['CDELT1'])
fwhm = 30./(pix_val*3600)
fwhmX = 60./(pix_val*3600)
fwhmY = 120./(pix_val*3600)

def symGaussian(size,fwhm=fwhm,center=None):
    """
    make a square gaussian kernel
    size is the length of the side of a square
    fwhm is the full width at half maximum which can be thought of as the effective radius
    center indicates where the gaussian should be centered
    
    Example
    symGaussian(10,fwhm=3,(50,50))
    """
    x = np.arange(0, size, 1, float)
    y = x[:,np.newaxis]
    sigma = fwhm/2.35
    
    if center is None:
        x0 = y0 = size // 2
    else:
        x0 = center[0]
        y0 = center[1]
    
    return np.exp(-(((x-x0)**2 + (y-y0)**2) / 2*sigma**2))

def varGaussian(gVal,fwhm=fwhm,center=None):
    """
    make a square gaussian kernel
    gVal is the gaussian value for whose x the size s twice
    fwhm is the full width at half maximum which can be thought of as the effective radius
    center indicates where the gaussian should be centered
    
    Example
    varGaussian(10,fwhm=3,(50,50))
    """
    sigma = fwhm/2.35
    upperLimit = np.sqrt(-2*(sigma**2)*np.log(gVal))
    lowerLimit = -np.sqrt(-2*(sigma**2)*np.log(gVal))
    size = 2*upperLimit
    
    x = np.arange(lowerLimit,size, 1, float)
    y = x[:,np.newaxis]
    
    if center is None:
        x0 = y0 = size // 2
    else:
        x0 = center[0]
        y0 = center[1]
    
    return np.exp(-(((x-x0)**2 + (y-y0)**2) / 2*sigma**2))

def asyGaussian(size,fwhmX=fwhmX, fwhmY=fwhmY, center=None):
    """
    make a square gaussian kernel
    size is the length of the side of a square
    fwhm is the full width at half maximum which can be thought of as the effective radius
    center indicates where the gaussian should be centered
    
    
    Example
    asyGaussian(10,fwhmX=3,fwhmY=9,(50,50))
    """
    sigmaX = fwhmX/2.35
    sigmaY = fwhmY/2.35
    x = np.arange(0, size, 1, float)
    y = x[:,np.newaxis]
    
    if center is None:
        x0 = y0 = size // 2
    else:
        x0 = center[0]
        y0 = center[1]
    
    return np.exp(-(((x-x0)**2/(2*sigmaX**2)) + ((y-y0)**2/(2*sigmaY**2))))

def rotateFunction(x,y,theta):
    c, s = np.cos(np.radians(theta)), np.sin(np.radians(theta))
    return x*c - y*s, x*s + y*c

def rotatedGaussian(theta,size,fwhmX=fwhmX,fwhmY=fwhmY,center=None):
    """ 
    Rotated asymmetric gaussian
    """
    sigmaX = fwhmX/2.35
    sigmaY = fwhmY/2.35
    x = np.arange(0,size, 1, float)
    y = x[:,np.newaxis]
    
    if center is None:
        x0 = y0 = size // 2
    else:
        x0 = center[0]
        y0 = center[1]
    
    xPrime, yPrime = rotateFunction(x,y,theta)[0],rotateFunction(x,y,theta)[1]
    
    return np.exp(-(((xPrime-x0)**2/(2*sigmaX**2)) + ((yPrime-y0)**2/(2*sigmaY**2))))
