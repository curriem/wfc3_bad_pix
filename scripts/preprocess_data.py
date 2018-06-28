import numpy as np
import glob
import cPickle as pickle
import astropy.io.fits as pyfits
import argparse

parser = argparse.ArgumentParser(description='Bad Pixel Data')
parser.add_argument('ims_path', help='path to directory of fits images')
parser.add_argument('save_file',
                    help='path and file name to save as, must be .p')
args = parser.parse_args()

set_data = {}
set_data['data'] = []
set_data['err'] = []
set_data['SAA_time'] = []
set_data['EXPEND'] = []
set_data['FILTER'] = []

ims = glob.glob(args.ims_path + '/*')

for im in ims:
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

pickle.dump(set_data, open(args.save_file, 'wb'))
