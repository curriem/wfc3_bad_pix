import numpy as np
import sys

pix_num = int(sys.argv[1])

map = np.zeros((1014, 1014))

map = map.flatten()

map[pix_num] = 1

map = map.reshape((1014, 1014))

i, j = np.where(map == 1)

print 'pixel number:', pix_num
print 'FITS coords (x, y):', j[0]+1, i[0]+1

