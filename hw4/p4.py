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

    # default to center at (0,0) if not provided
    if center is not None:
        a, b = center
    else:
        a, b = 0, 0

    # the gaussian function
    res = (-(x-a)**2 + (y-b)**2) / (2*(sigma**2))

    return np.exp(res)

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
    
    M, N = shape # shape of original image

    # make a meshgrid of integers [0,M]x[0,N]
    mesh_x = np.arange(M)
    mesh_y = np.arange(N)
    mesh = np.meshgrid(mesh_y, mesh_x)
    
    # result is a discrete gaussian filter ...
    g_kern = gaussian(mesh, sigma, center=(N/2, M/2))

    # ... with the same shape as the original image
    assert g_kern.shape == shape

    # return mesh for plotting
    return g_kern, mesh


if __name__ == "__main__":
    
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
    
    # create discrete gaussian filter
    g_kern, g_mesh = gaussian_filter(img.shape, sigma=15)

    # g_kern is centered, so use shifted FT of image
    convolute = g_kern * fss

    # shift back and reverse transform to get the filtered image
    filtered = ifft2(ifftshift(convolute))

    # actually, any nonreal components must be from roundoff
    f_img = filtered.real

    print('max bound on imaginary error:')
    print('\t np.abs(filtered.imag).max()=', np.abs(filtered.imag).max())
    
    # create fourier spectra to view as images
    img_spectrum = np.log10(np.abs(fss))
    conv_spectrum = np.log10(np.abs(convolute))

    # plot these
    fig, ax = plt.subplots(2,2)
    ax[0,0].imshow(img, cmap='gray')
    ax[0,0].set_title('(a)', fontsize='large')

    # default (nongrey) colormap is actualy easier to see
    ax[0,1].imshow(img_spectrum)
    ax[0,1].set_title('(b)', fontsize='large')

    ax[1,0].imshow(conv_spectrum)
    ax[1,0].set_title('(c)', fontsize='large')

    ax[1,1].imshow(f_img, cmap='gray')
    ax[1,1].set_title('(d)', fontsize='large')
    
    fig.show()
    # EXTRANEOUS ______________________________
    # plot gaussian used

    fig2 = plt.figure()
    ax2 = fig2.gca(projection='3d')
    ax2.plot_surface(g_mesh[0], g_mesh[1], g_kern)
    ax2.set_alpha(0)
    fig2.savefig('p4-gaussian15.png')

    #bx2 = fig2.add_subplot(222)

    #bx2.imshow(g_kern)

    #bx3 = fig2.add_subplot(223)
    #bx4 = fig2.add_subplot(224)


    ## make histograms of the cropped region for the original image and the result
    #S = crop_range(img)
    #img_crop = img[S].round()
    #filtered_crop = f_img[S].round()

    #orig = np.histogram(img_crop.flatten(), bins=256)[0]
    #filt = np.histogram(filtered_crop.flatten(), bins=256)[0]
    #bx3.bar(range(256), orig)
    #bx4.bar(range(256), filt)
