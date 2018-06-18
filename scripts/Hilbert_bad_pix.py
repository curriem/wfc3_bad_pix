import astropy.io.fits as pyfits
import numpy as np
import matplotlib.pyplot as plt


fl = pyfits.open('../data/w681807ii_bpx.fits')
data = fl[1].data

x = data['PIX1']
y = data['PIX2']
c = data['VALUE']

inds = np.less(x, 1) | np.greater(x, 1014) | np.less(y, 1) | np.greater(y, 1014)


np_x = y[~inds] - 1
np_y = x[~inds] - 1
val = c[~inds]
inds_512 = np.where(val == 512)
val[inds_512] = 0

val = val.astype(bool)

H_bad_pix_map = np.zeros((1014, 1014), dtype=bool)

H_bad_pix_map[np_x, np_y] = val


C_bad_pix_map = np.load('../data/C_bad_pix_map.npy')

C_bad_pix_map = C_bad_pix_map.astype(bool)
H_bad_pix_map = H_bad_pix_map.astype(bool)
np.save('../data/H_bad_pix_map.npy', H_bad_pix_map)
agreement_bad_pix_map = C_bad_pix_map & H_bad_pix_map

plt.figure()
plt.imshow(H_bad_pix_map, origin='lower')
plt.title('Hilbert, %s bad pix' % str(np.sum(H_bad_pix_map)))
plt.figure()
plt.imshow(C_bad_pix_map, origin='lower')
plt.title('Currie, %s bad pix' % str(np.sum(C_bad_pix_map)))
plt.figure()
plt.imshow(agreement_bad_pix_map, origin='lower')
plt.title('agreement, %s bad pix' % str(np.sum(agreement_bad_pix_map)))
plt.show()



print inds
