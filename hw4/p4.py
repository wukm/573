#!/usr/bin/env python3

from scipy.fftpack import fft2, ifft2, fftshift, fftfreq
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import PIL.Image

# note that this file is RGB but all three channels are equal, so we can convert
# it to grayscale easily. fix this later for real RGB stuff
IMAGE_FILE = "lena_noisy.png"

def gaussian_filter(x, y):

    sigma = 0.8 # variance
    a,b = 0,0 # center

    return np.exp(-((x-a)**2 + (y-b)**2) / (2*sigma**2))


img_raw = PIL.Image.open(IMAGE_FILE)
img_raw = img_raw.convert('L') # convert to grayscale
img = np.array(img_raw, dtype='f')
#img /= 255 #scale between 0 and 1, maybe unnecessary

fs = fft2(img)

fss =  fftshift(fs) # shift it so high freq stuff is in the center


mesh_x = np.linspace(-10,10,num=fs.shape[0])
mesh_y = np.linspace(-10,10,num=fs.shape[1])    
kern = np.meshgrid(mesh_y,mesh_x)
g_kern = gaussian_filter(*kern)
g_kern /= g_kern.sum() # normalize for fun?
stuff = fftshift(g_kern * fss) # elementwise multiplication in the frequency domain

result = ifft2(stuff)

# i dunno at all. make the complex fft something you can look at?
mag = np.log(np.abs(fss))
mag2 = np.log(np.abs(stuff))
mag3 = np.log(np.abs(result))

# make a 2x2 plot and give all the subaxes names for ease
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2)


ax1.imshow(img_raw, cmap=cm.Greys_r)
ax2.imshow(mag) # default (nongrey) colormap is actualy easier to see
ax3.imshow(mag2)
ax4.imshow(mag3, cmap=cm.Greys_r)

#fig.show()
fig.savefig('prob4.png')
