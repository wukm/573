#!/usr/bin/env python3

import numpy as np
from scipy.fftpack import fft2, ifft2, fftshift, ifftshift, fftfreq
import PIL.Image

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D


def crop_range(A, border_val=255):
    """
    returns a slice object that would remove a border about a subimage.
    That is, these indices indicate the 'subimage' part of A. See example below. 
    Note that this border_val is found via equality only.
    
    For now, A must be a 2D array. 

    INPUT
    A:   a 2D numpy.array
    border_val: the "border val" to be cropped out (default 255)
    
    OUTPUT:
    s: a slice object such that A[s] is the subimage.

    Example:

        A = np.array([[0, 1, 2, 0, 0],
                    [0, 0, 1, 3, 0],
                    [0, 1, 3, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0]])

        s = crop_range(A, 0)

        A[s]
        >>> array([[1, 2, 0],
                [0, 1, 3],
                [1, 3, 0]])

    """

    # can rewrite for arbitrary dim: store in a N x 2 array and iterate, but
    # making slice object needs some thought
    # note this current implementation may be inefficient for large matrices

    for i_start in range(A.shape[0]):
        if not all(A[i_start] == border_val):
            break

    for i_end in range(-1, -A.shape[0] -1, -1):
        if not all(A[i_end] == border_val):
            break
    
    for j_start in range(A.shape[1]):
        if not all(A[:,j_start] == border_val):
            break

    for j_end in range(-1, -A.shape[1] - 1, -1):
        if not all(A[:,j_end] == border_val):
            break

    # return a slice object S such that A[S] is the subimage
    return np.s_[i_start:i_end+1 , j_start:j_end+1]

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

def gaussian_filter(shape, sigma):
    """
    creates a discrete gaussian filter of shape `shape` with variance `sigma`
    centered in the middle. Note that this filter is not normalized in any way.
    
    INPUT:
    
    shape:  a tuple representing the size of the filter
    sigma:  variance for the gausian function (a scalar)
    
    OUTPUT:

    G:  a discrete gaussian filter with G.shape == `shape`

    """
    
    M, N = shape
    mesh_x = np.arange(M)
    mesh_y = np.arange(N)

    mesh = np.meshgrid(mesh_y, mesh_x)

    g_kern = gaussian(mesh, sigma, center=(N/2, M/2))

    assert g_kern.shape == shape

    return g_kern, mesh


if __name__ == "__main__":
    
    img_raw = PIL.Image.open('./lena_noisy.png')

    # convert to grayscale, all channels are equal (should verify?)
    img_raw = img_raw.convert('L')
    img = np.array(img_raw, dtype='f')

    fs = fft2(img)
    fss = fftshift(fs)

    g_kern, g_mesh = gaussian_filter(img.shape, sigma=15)

    # g_kern is centered, so use shifted FT of image
    convolute = g_kern * fss

    # shift back and reverse transform
    filtered = ifft2(ifftshift(convolute))


    # actually, any nonreal components must be from roundoff
    f_img = filtered.real

    print('imaginary error accumulated:')
    print('\t np.abs(filtered.imag).max()=', np.abs(filtered.imag).max())
    
    img_spectrum = np.log10(np.abs(fss))

    fimg_spectrum = np.log10(np.abs(convolute))

    # make a 2x2 plot and give all the subaxes names for ease

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2)


    ax1.imshow(img, cmap=cm.Greys_r)

    # default (nongrey) colormap is actualy easier to see
    ax2.imshow(img_spectrum)
    ax3.imshow(conv_spectrum)
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
    bx3.bar(range(256), orig)
    bx4.bar(range(256), filt)

    fig2.show()
