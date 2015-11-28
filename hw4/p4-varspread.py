#!/usr/bin/env python3

import numpy as np
from scipy.fftpack import fft2, ifft2, fftshift, ifftshift, fftfreq
import PIL.Image

import matplotlib.pyplot as plt

from p4 import *

plt.style.use('seaborn-paper')
plt.set_cmap('viridis')

img_raw = PIL.Image.open('./lena_noisy.png')

img = np.array(img_raw, dtype='f')

# convert image to greyscale if it's 3 channels, else stop.
if img.ndim == 3 and img.shape[-1] == 3:
    # all three channels are equal
    if (img[:,:,0] == img[:,:,1]).all() and (img[:,:,1] == img[:,:,2]).all():
        img = img[:,:,0] # keep only one
    else:
        raise Exception("cannot convert to single channel")

elif img.ndim == 1:
    pass # one channel, so we're fine
else:
    raise Exception("cannot handle this image.")

fs = fft2(img) # 2D fourier transform of the image
fss = fftshift(fs) # shift low frequency stuff to center

S = crop_range(img)

sigmas = [None, 2, 5, 15, 25, 35]
fig, axes = plt.subplots(2,3)
h_fig, h_axes = plt.subplots(2,3)

for s, ax, hx in zip(sigmas, axes.flatten(), h_axes.flatten()):

    if s is not None:
        g_kern, _ = gaussian_filter(img.shape, sigma=s)
        title = r'$\sigma = {}$'.format(s) 
    else:
        # do nothing to the spectrum
        g_kern = np.ones_like(img)
        title = 'original'

    convolute = g_kern * fss
    filtered = ifft2(ifftshift(convolute))

    f_img = filtered.real

    ax.imshow(f_img[S], cmap='gray')
    ax.set_axis_off()
    
    ax.set_title(title, fontsize='large')

    ## make histograms of the cropped region for the original image and the result
    filtered_crop = f_img[S].round()

    filt = np.histogram(filtered_crop.flatten(), bins=256)[0]
    hx.bar(range(256), filt, width=1, fc='k',ec='k')
    hx.set_xbound(0,256+16)
    hx.tick_params(axis='y', labelleft='off', direction='out', right='off')
    hx.set_title(title, fontsize='large')

    h_fig.show()

