import matplotlib.pyplot as plt
import numpy as np

book_path = '/Volumes//My_Book/wfc3_bad_pix/data/'

bad_pix_2014a1 = np.loadtxt(book_path + '/darks/bad_pix_list_2014a.txt',
                            dtype=np.int)
bad_pix_2014b1 = np.loadtxt(book_path + '/darks/bad_pix_list_2014b.txt',
                            dtype=np.int)
bad_pix_2014a2 = np.loadtxt(book_path + '/flats/bad_pix_list_2014a.txt',
                            dtype=np.int)
bad_pix_2014b2 = np.loadtxt(book_path + '/flats/bad_pix_list_2014b.txt',
                            dtype=np.int)
bad_pix_orig =\
    np.loadtxt('/Users/mcurrie/GitRepos/step_1/bad_pix_list_wfc3.txt',
               dtype=np.int)

bad_pix_new1 = np.concatenate((bad_pix_2014a1, bad_pix_2014b1))
bad_pix_new1 = np.unique(bad_pix_new1, axis=0)
bad_pix_new2 = np.concatenate((bad_pix_2014a2, bad_pix_2014b2))
bad_pix_new2 = np.unique(bad_pix_new2, axis=0)

bad_pix_new = np.concatenate((bad_pix_new1, bad_pix_new2))
bad_pix_new = np.unique(bad_pix_new, axis=0)

map = np.zeros((1014, 1014))
bad_pix_all = np.empty((0, 2))
for coords in bad_pix_new1:
    map[coords[0], coords[1]] += 1
    bad_pix_all = np.concatenate((bad_pix_all, [[coords[0], coords[1]]]))

for coords in bad_pix_new2:
    map[coords[0], coords[1]] += 1
    bad_pix_all = np.concatenate((bad_pix_all, [[coords[0], coords[1]]]))

for coords in bad_pix_orig:
    map[coords[1] - 1, coords[0] - 1] += 2
    bad_pix_all = np.concatenate((bad_pix_all, [[coords[1]-1, coords[0]-1]]))


print 'Num pix in common:',len(bad_pix_all) -len(np.unique(bad_pix_all, axis=0))
print 'Num pix orig:', len(bad_pix_orig)
print 'Num pix new:', len(bad_pix_new1) + len(bad_pix_new2)

plt.figure()
plt.imshow(map, origin='lower', cmap='Greys')
plt.axis('off')
plt.colorbar()
plt.show()
