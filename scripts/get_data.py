import numpy as np
import glob
import sys
import cPickle as pickle
import astropy.io.fits as pyfits

#exp_type = sys.argv[1]

#sets = glob.glob('/Volumes/My_Book/wfc3_bad_pix/data/%s/set_*' % exp_type)

sets = glob.glob('../data/set_Hilbert*')

for set in sets:
    year = set.split('_')[-1]
    set_data = {}
    set_data['data'] = []
    set_data['err'] = []
    set_data['SAA_time'] = []
    set_data['EXPEND'] = []
    set_data['FILTER'] = []

    ims = glob.glob(set + '/*fits')

    for im in ims:
        print im
        data = pyfits.getdata(im, ext=1, memmap=False)
        err = pyfits.getdata(im, ext=2, memmap=False)
        SAA_time = pyfits.getval(im, 'SAA_TIME')
        EXPEND = pyfits.getval(im, 'EXPEND')
        FILTER = pyfits.getval(im, 'FILTER')
        set_data['data'].append(data)
        set_data['err'].append(err)
        set_data['SAA_time'].append(SAA_time)
        set_data['EXPEND'].append(EXPEND)
        set_data['FILTER'].append(FILTER)

    for key in set_data.keys():
        set_data[key] = np.array(set_data[key])
    # save_path = '/Volumes/My_Book/wfc3_bad_pix/data/%s/data_%s_%s.p' \
    #         % (exp_type, exp_type, year), 'wb')
    save_path = '../data/data_%s.p' % year
    pickle.dump(set_data, open(save_path, 'wb'))
