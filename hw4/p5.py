#!/usr/bin/env python3

import numpy as np
from scipy.fftpack import fft2, ifft2, fftshift, ifftshift
import PIL.Image

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D

from p4 import gaussian_filter


EINSTEIN = "einstein.png"
MARILYN = "marilyn.png"

if __name__ == "__main__":

    # convert each to grayscale
    einstein = PIL.Image.open(EINSTEIN).convert('L')
    marilyn = PIL.Image.open(MARILYN).convert('L')

    einstein = np.array(einstein, dtype='f')
    marilyn = np.array(marilyn, dtype='f')
    
    # make sure we can combine these images directly
    assert einstein.shape == marilyn.shape

    ft_e = fft2(einstein)
    ft_m = fft2(marilyn)
    
    # shift so hi-freq stuff is in the center
    ft_e = fftshift(ft_e) 
    ft_m = fftshift(ft_m) 

    # use gaussian filter as a low pass filter
    flo, _ = gaussian_filter(einstein.shape, sigma=10)
    
    fhi = 1 - flo
    
    lo_e = ifft2(ifftshift(flo * ft_e))
    hi_m = ifft2(ifftshift(fhi * ft_m))
    
    lo_m = ifft2(ifftshift(flo * ft_m))
    hi_e = ifft2(ifftshift(fhi * ft_e))
    
    hybrid = lo_e + hi_m 
    hybrid_rev = lo_m + hi_e

    # make a 2x2 plot and give all the subaxes names for ease
    fig, ((ax1, ax2, ax3, ax4)) = plt.subplots(1,4)

    ax1.axis('off')
    ax2.axis('off')
    ax3.axis('off')
    ax4.axis('off')

    ax1.imshow(einstein, cmap=cm.gray)
    ax2.imshow(marilyn, cmap=cm.gray)
    ax3.imshow(hybrid.real, cmap=cm.gray)
    ax4.imshow(hybrid_rev.real, cmap=cm.gray)

    fig.show()

