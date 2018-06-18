import numpy as np
import matplotlib.pyplot as plt
import astropy.io.fits as pyfits

impath = './Hilbert_2012im1.fits'
C_bad_pix_map = np.load('../data/C_bad_pix_map.npy')
H_bad_pix_map = np.load('../data/H_bad_pix_map.npy')
im = pyfits.getdata(impath, 1)

size = 50
xstart = 1
ystart = 1


fig, axes = plt.subplots(1, 2,
                         figsize=(7, 5))

im_crop = im[ystart-1:ystart-1 + size, xstart-1:xstart-1 + size]
im_crop = np.clip(im_crop, -0.5, 2)

Cmap_crop = C_bad_pix_map[ystart-1:ystart-1 + size, xstart-1:xstart-1 + size]
Hmap_crop = H_bad_pix_map[ystart-1:ystart-1 + size, xstart-1:xstart-1 + size]


x_len, y_len = im_crop.shape
Hx = []
Hy = []
Cx = []
Cy = []

for x in range(x_len):
    for y in range(y_len):
        if Hmap_crop[x, y]:
            Hx.append(x)
            Hy.append(y)
        if Cmap_crop[x, y]:
            Cx.append(x)
            Cy.append(y)

axes[0].imshow(im_crop, origin='lower', cmap='gray',
               interpolation='nearest',
               aspect='equal')
axes[0].scatter(Hy, Hx,
                marker='s', facecolors='none',
                s=9,
                edgecolors='lime',
                linewidth=0.5)
axes[1].imshow(im_crop, origin='lower', cmap='gray',
               interpolation='nearest',
               aspect='equal')
axes[1].scatter(Cy, Cx,
                marker='s', facecolors='none',
                s=9,
                edgecolors='lime',
                linewidth=0.5)
axes[0].set_title('Hilbert 2012\nCycles 17, 18, and 19 darks')
axes[1].set_title('Currie 2018\nCycles 17, 18, and 19 darks')
plt.tight_layout()
for axis in axes:
    axis.axis('off')
plt.savefig('../plots/H_C_compare_im.pdf', bbox_inches='tight')

