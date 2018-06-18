import numpy as np
import cPickle as pickle
import glob
import astropy.io.fits as pyfits

#hd_path = '/Volumes/My_Book/wfc3_bad_pix/data/'
hd_path = '../data/'
#sets = glob.glob(hd_path+'/flats/set_2018*')
sets = glob.glob(hd_path+'/set_Hilbert*')
for set in sets:
    year = set.split('_')[-1]
    ims = glob.glob(set + '/*')
    filters = []
    for im in ims:
        print im, 'SAA_TIME', pyfits.getval(im, 'SAA_TIME')
        '''
        filters.append(pyfits.getval(im, 'FILTER'))

    filters = np.array(filters)
    print filters
    pkl = pickle.load(open(hd_path+'/flats/data_flats_'
                           + year + '.p', 'rb'))
    pkl['filter'] = filters
    pickle.dump(pkl, open(hd_path+'/flats/data_flats_'
                          + year + '.p', 'wb'))
                          '''
