# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 09:21:03 2016

@author: samuel
"""

import numpy as np
from matplotlib import pylab as plt

def gaussian(x, a, mu, sig):
    return a*np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def plotgaussian(a, mu, sigma):

    # Plotting range
    xrange = [mu-4.*sigma,mu+4.*sigma]

    # Create Gaussian
    x = np.linspace(xrange[0], xrange[1], 900)
    y = gaussian(x, a, mu, sigma)
    
    # To illustrate the meaning of sigma calculate mu+sigma and mu-sigma
    siglleft = mu-sigma
    siglright = mu+sigma
    sigh = gaussian(mu+sigma, a, mu, sigma)

    # To plot FWHM arrows calculate mu+HWHM and mu-HWHM
    hwhmleft = -np.sqrt(2.*np.log(2.))*sigma+mu
    hwhmright = np.sqrt(2.*np.log(2.))*sigma+mu
    hm = a/2.

    # Start the plot, create a figure instance and a subplot
    fig = plt.figure()
    ax  = fig.add_subplot(111)

    # Axis ranges
    ax.axis([mu-4.*sigma, mu+4.*sigma, -a*0.1, a*1.1])

    # Plot a grid
    ax.grid(True)

    # Insert lines at x=0 and y=0
    ax.axhline(0.,linewidth=1, color = 'k', linestyle='dashed')
    ax.axvline(0.,linewidth=1, color = 'k', linestyle='dashed')

    # Draw a line to mark the position a
    ax.plot([mu,mu],[0.,a], 'g-')

    # Draw lines for sigma area
    ax.plot([siglleft, siglleft],[0.,sigh], 'b--')
    ax.plot([siglright, siglright],[0.,sigh], 'b--')

    # Draw line to show amplitude
    ax.plot([mu, mu+2*sigma],[a,a], 'm--')


    # Plot the function
    ax.plot(x,y, 'k-')

    # Show amplitude
    plt.annotate(s='', xy=(mu+2*sigma,0.), xytext=(mu+2*sigma,a), \
                 arrowprops=dict(color = 'magenta', arrowstyle='<->'))
    ax.text(mu+2*sigma+sigma/10., a/2, '$a$', fontsize = 12, horizontalalignment = 'left', \
            verticalalignment = 'center', color = 'magenta')

    # Overplot FHHM
    plt.annotate(s='', xy=(hwhmleft,hm), xytext=(hwhmright,hm), \
                 arrowprops=dict(color = 'red', arrowstyle='<->'))
    ax.text(mu, hm, 'FWHM', fontsize = 12, horizontalalignment = 'center', \
            verticalalignment = 'top', color = 'red')

    # Overplot sigma
    plt.annotate(s='', xy=(siglleft,sigh), xytext=(mu,sigh), arrowprops=dict(color = 'blue', arrowstyle='<->'))
    ax.text((siglleft+mu)/2, sigh, '$\sigma$', fontsize = 12, \
            horizontalalignment = 'center', verticalalignment = 'top', color = 'blue')
    plt.annotate(s='', xy=(siglright,sigh), xytext=(mu,sigh), arrowprops=dict(color = 'blue', arrowstyle='<->'))
    ax.text((siglright+mu)/2, sigh, '$\sigma$', fontsize = 12, \
            horizontalalignment = 'center', verticalalignment = 'top', color = 'blue')

    # Mark position of mu
    ax.text(mu, 0., '$\mu$', fontsize = 12, \
            horizontalalignment = 'center', verticalalignment = 'top', color = 'green')
    
    #Formula
    ax.text(mu-3.8*sigma, a/2, r'$a e^{-\frac{(x-\mu)^2}{2\sigma^2}}$', fontsize = 20, \
            horizontalalignment = 'left', verticalalignment = 'top', color = 'black')

    plt.title("Gaussian", fontsize=14,color='black')
    
plotgaussian(2., 1., 1.)
plotgaussian(1/(np.sqrt(2.*np.pi)), 0., 1.)