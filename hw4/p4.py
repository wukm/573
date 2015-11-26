#!/usr/bin/env python3


import numpy as np
from scipy.fftpack import fft2, ifft2, fftshift, ifftshift, fftfreq
import PIL.Image

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D


IMAGE_FILE = "./lena_noisy.png"

def crop_range(A, border_val=255):
    """
    returns a slice such that A[ind] is a matrix with a border removed.
    that is, these indices indicate the 'subimage' part of A.
    be careful to round first, since border is identified by equality with
    border_val
    """
    # this is needlessly wasteful. only need the first and last one of each
    # maybe mask out the border_val and just find argmax, argmin for each axis
    a, b = np.where(A != border_val)
    
    # return a slice object S such that A[S] is the subimage
    return np.s_[a[0]:a[-1]+1 , b[0]:b[-1]+1]

def gaussian(point, sigma, center=None):
    """
    the 2D gaussian of points x, y = point
    with variance sigma and center a,b = center (defaults to (0,0))
    """
    if center is not None:
        a, b = center
    else:
        a, b = 0, 0
    x, y = point
    res = (x-a)**2 + (y-b)**2
    res = (-res)/(2*(sigma**2))
    res = np.exp(res)

    return res

#def gaussian_filter(shape, sigma, center=None):
#    """
#    shape is shape of image you wish to filter
#    """
#    
#    # zero centered integer steps the same shape as the original image 
#    mesh_x = np.arange(shape[0], dtype=np.float) - shape[0]//2
#    mesh_y = np.arange(shape[1], dtype=np.float) - shape[1]//2
#    
#    step_scale = sigma * np.sqrt(2)
#    mesh_x /= step_scale
#    mesh_y /= step_scale 
#
#    mesh = np.meshgrid(mesh_y, mesh_x)
#    
#    g_kern = gaussian(mesh, sigma)
#
#    k = np.sqrt( 2*np.pi) * sigma
#    g_kern /= k
#
#    assert g_kern.shape == shape
#    #g_kern /= g_kern.sum()
#    # return mesh for graphing purposes
#    return g_kern, mesh

def gaussian_filter(shape, sigma, center=None):
    
    M, N = shape
    mesh_x = np.arange(M)
    mesh_y = np.arange(N)

    mesh = np.meshgrid(mesh_y, mesh_x)

    g_kern = gaussian(mesh, sigma, center=(N/2, M/2))

    assert g_kern.shape == shape

    return g_kern, mesh

img_raw = PIL.Image.open(IMAGE_FILE)
img_raw = img_raw.convert('L') # convert to grayscale, all channels are equal
img = np.array(img_raw, dtype='f')

fs = fft2(img)
fss = fftshift(fs)
g_kern, g_mesh = gaussian_filter(img.shape, sigma=15)

convolute = g_kern * fss
filtered = ifft2(ifftshift(convolute))

print('imaginary error accumulated:')
print('\t np.abs(filtered.imag).max()=', np.abs(filtered.imag).max())
f_img = filtered.real

# actually, any nonreal components must be from roundoff
mag = np.log10(np.abs(fss))

mag2 = np.log10(np.abs(convolute))

# make a 2x2 plot and give all the subaxes names for ease

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2)


ax1.imshow(img, cmap=cm.Greys_r)
ax2.imshow(mag) # default (nongrey) colormap is actualy easier to see
ax3.imshow(mag2)
ax4.imshow(f_img, cmap=cm.Greys_r)

fig.show()

fig2 = plt.figure()
bx1 = fig2.add_subplot(221, projection='3d')
bx1.plot_surface(g_mesh[0], g_mesh[1], g_kern)

bx2 = fig2.add_subplot(222)

bx2.imshow(g_kern)

bx3 = fig2.add_subplot(223)
bx4 = fig2.add_subplot(224)


# make histograms of the cropped region for the original image and the result
S = crop_range(img)
img_crop = img[S].round()
filtered_crop = f_img[S].round()

orig = np.histogram(img_crop.flatten(), bins=256)[0]
filt = np.histogram(filtered_crop.flatten(), bins=256)[0]
bx3.plot(range(256), orig)
bx4.plot(range(256), filt)

fig2.show()
