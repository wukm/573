#!/usr/bin/env python3

from scipy.fftpack import fft2, ifft2, fftshift, fftfreq, ifftshift
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import PIL.Image

# note that this file is RGB but all three channels are equal, so we can convert
# it to grayscale easily. fix this later for real RGB stuff
EINSTEIN = "einstein.png"
MARILYN = "marilyn.png"

def gaussian_filter(x, y):

    sigma = 0.4 # variance
    a,b = 0,0 # center

    return np.exp(-((x-a)**2 + (y-b)**2) / (2*sigma**2))


# convert each to grayscale
einstein = PIL.Image.open(EINSTEIN).convert('L')
marilyn = PIL.Image.open(MARILYN).convert('L')

einstein = np.array(einstein, dtype='f')
marilyn = np.array(marilyn, dtype='f')
#einstein /= 255
#marilyn /= 255

ft_e = fft2(einstein)
ft_m = fft2(marilyn)

assert ft_e.shape == ft_m.shape

ft_e = fftshift(ft_e) # shift it so high freq stuff is in the center
ft_m = fftshift(ft_m) # shift it so high freq stuff is in the center


mesh_x = np.linspace(-10,10,num=ft_e.shape[0])
mesh_y = np.linspace(-10,10,num=ft_e.shape[1])    
kern = np.meshgrid(mesh_y,mesh_x)

def linearize(A):

    return (A - A.min()) / (A.max() - A.min())

g_kern_low = gaussian_filter(*kern)

g_kern_low = linearize(g_kern_low)
g_kern_low /= g_kern_low.sum() # normalize for fun?


#g_kern_hi = 1 - gaussian_filter(*kern)
#g_kern_hi /= g_kern_hi.sum() # normalize for fun?
g_kern_hi = 1 - g_kern_low

# try fftshift?
stuff = ifftshift(g_kern_hi * ft_e) # elementwise multiplication in the frequency domain
stuff2 = ifftshift(g_kern_low * ft_m)

result = np.log(abs(ifft2(stuff)))
result += np.log(np.abs(ifft2(stuff2)))
mag = linearize(result)

# make a 2x2 plot and give all the subaxes names for ease
fig, ((ax1, ax2, ax3, ax4)) = plt.subplots(1,4)

ax1.axis('off')
ax2.axis('off')
ax3.axis('off')
ax4.axis('off')

ax1.imshow(einstein, cmap=cm.gray)
ax2.imshow(marilyn, cmap=cm.gray)
ax3.imshow(mag, cmap=cm.gray)

# now reverse?
stuff_rev = fftshift(g_kern_low * ft_e) # elementwise multiplication in the frequency domain
stuff2_rev = fftshift(g_kern_hi * ft_m)

result_rev = np.log(np.abs(ifft2(stuff_rev)))
result_rev += np.log(np.abs(ifft2(stuff2_rev)))

# i dunno at all. make the complex fft something you can look at?
mag2 = result_rev
ax4.imshow(mag2, cmap=cm.gray)
fig.show()
