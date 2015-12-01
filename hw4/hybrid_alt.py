#!/usr/bin/env python3

import numpy as np
from scipy.fftpack import fft2, ifft2, fftshift, ifftshift
import PIL.Image

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D

from p4 import gaussian_filter


CAT = "cat.png"
EARTH = "marble.png"

if __name__ == "__main__":

    # convert each to grayscale
    cat = PIL.Image.open(CAT).convert('L')
    earth = PIL.Image.open(EARTH).convert('L')
    
    cat = np.array(cat, dtype='f')
    earth = np.array(earth, dtype='f')
    
    # make sure we can combine these images directly
    assert cat.shape == earth.shape
    
    # take fourier transforms
    ft_e = fft2(cat)
    ft_m = fft2(earth)
    
    # shift so hi-freq stuff is in the center
    ft_e = fftshift(ft_e) 
    ft_m = fftshift(ft_m) 

    # use gaussian filter as a low pass filter
    flo, _ = gaussian_filter(cat.shape, sigma=15)
    
    # create a high pass filter
    fhi = 1 - flo
    
    # lowpass on earth, high-pass on cat
    lo_e = ifft2(ifftshift(flo * ft_e))
    hi_m = ifft2(ifftshift(fhi * ft_m))
    
    # high pass on earth, low-pass on cat
    lo_m = ifft2(ifftshift(flo * ft_m))
    hi_e = ifft2(ifftshift(fhi * ft_e))
    
    hybrid = lo_e + hi_m 
    hybrid_rev = lo_m + hi_e
    
    # plotting stuff ################################

    # make a 2x2 plot and give all the subaxes names for ease
    fig, ((ax1, ax2, ax3, ax4)) = plt.subplots(1,4)

    ax1.axis('off')
    ax2.axis('off')
    ax3.axis('off')
    ax4.axis('off')

    ax1.imshow(cat, cmap=cm.gray)
    ax2.imshow(earth, cmap=cm.gray)
    ax3.imshow(hybrid.real, cmap=cm.gray)
    ax4.imshow(hybrid_rev.real, cmap=cm.gray)
