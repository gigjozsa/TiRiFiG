# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 09:36:43 2016

@author: samuel
"""

import math
import numpy as np
from matplotlib import pylab as plt

from matplotlib import rcParams
rcParams['text.usetex'] = True

#def trianglewave(x, T):
#    """
#    This is a sawtooth, though
#    """
#    return np.mod(x/T,1.)*np.logical_and(x>=0,x<=T)

def trianglewave(x, T):
    """
    T is the period.
    """
    return np.abs(2.*(np.mod(x/T,1.)-0.5))-0.5

def boxcar(x,a,b,amp):
    return amp*np.logical_and(x>=a,x<=b)
    
def plottriboxconv(a, b, period):

    # limits of boxcar Play arround with this
#    a = -0.1
#    b = 0.1
    
    # Plotting range
    xrange = [-2., 2.]

    # Create functions
    xpoints = 1000
   
    # Resolution element
    dx = (xrange[1]-xrange[0])/float(xpoints)

    x = np.linspace(xrange[0], xrange[1], xpoints)
    y = boxcar(x, a, b, 1.)

    # boxcar will be normalised to 1. amp = 1./(b-a) works in the limit of many points, but here we do
    # numberofpixelsinbox*dx*amplitude = y.sum *dx*amplitude = 1
    # to take into account numerical effects
    amp = float(xpoints)/((xrange[1]-xrange[0])* y.sum())
    y = boxcar(x, a, b, 1./(b-a))
    ycorr = boxcar(x, a, b, amp)
    z = trianglewave(x, period)

    result = np.convolve(ycorr,z,'same')
    result = dx*result
        
    # Start the plot, create a figure instance and a subplot
    fig = plt.figure()
    ax1  = fig.add_subplot(311)
    fig.tight_layout()
    plt.subplots_adjust(hspace = 0.6)
    
    # Axis ranges
    ax1.axis([xrange[0]+(b-a), xrange[1]-(b-a), z.min()-0.1*(z.max()-z.min()), z.max()+0.1*(z.max()-z.min())])

    # Plot a grid
    ax1.grid(True)

    # Insert lines at x=0 and y=0
    ax1.axhline(0.,linewidth=1, color = 'k', linestyle='dashed')
    ax1.axvline(0.,linewidth=1, color = 'k', linestyle='dashed')
    
    # Plot function
    ax1.plot(x,z,'b-')

    plt.title("Triangle wave", fontsize=14,color='black')
    
    ax2  = fig.add_subplot(312, sharex=ax1) 

    # Axis ranges
    ax2.axis([xrange[0]+(b-a), xrange[1]-(b-a), ycorr.min()-0.1*(ycorr.max()-ycorr.min()), \
              ycorr.max()+0.1*(ycorr.max()-ycorr.min())])

    # Plot a grid
    ax2.grid(True)

    # Insert lines at x=0 and y=0
    ax2.axhline(0.,linewidth=1, color = 'k', linestyle='dashed')
    ax2.axvline(0.,linewidth=1, color = 'k', linestyle='dashed')
    
    # Plot function
    e1 = int(math.ceil(xpoints*(a-xrange[0])/(xrange[1]-xrange[0])))
    ax2.plot(x[:e1],y[:e1],'b-')
    ax2.plot([a, a],[0., amp],'b--')
    e2 = int(math.floor(xpoints*(b-xrange[0])/(xrange[1]-xrange[0])))
    ax2.plot(x[e1:e2],y[e1:e2],'b-')
    e3 = xpoints
    ax2.plot(x[e2:],y[e2:],'b-')
    ax2.plot([b, b],[0., amp],'b--')

    plt.title("Rectangle function", fontsize=14,color='black')
    
    ax3  = fig.add_subplot(313, sharex=ax2) 

    # Axis ranges: mask out border effects
    rmin = result.min()
    rmax = result.max()
    
    # Just to make the result a bit more beautiful if the function is very flat
    if (rmax - rmin) < 0.1:
        rmin=rmin-0.1
        rmax=rmax+0.1

    ax3.axis([xrange[0]+(b-a), xrange[1]-(b-a), rmin-0.1*(rmax-rmin), rmax+0.1*(rmax-rmin)])

    # Plot a grid
    ax3.grid(True)

    # Insert lines at x=0 and y=0
    ax3.axhline(0.,linewidth=1, color = 'k', linestyle='dashed')
    ax3.axvline(0.,linewidth=1, color = 'k', linestyle='dashed')
    
    # Plot function
    plr1 =  int(xpoints*(b-a)/(xrange[1]-xrange[0]))
    plr2 =  int(xpoints*(1-(b-a)/(xrange[1]-xrange[0])))
    
    ax3.plot(x[plr1:plr2],result[plr1:plr2],'b-')

    plt.title("Triangle wave filtered with rectangle function", fontsize=14,color='black')
        
# first two arguments give the position of the rectangle, third the period of the Triangle
plottriboxconv(-0.1, 0.1, 1.0)