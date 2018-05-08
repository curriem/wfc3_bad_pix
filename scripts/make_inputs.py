import numpy as np
import cPickle as pickle
import sys


def preprocess_data(data_pkl):
    N_im, i, j = data_pkl['data'].shape

    for n in range(N_im):
        data_pkl['err'][n, :, :] /= np.nanmedian(data_pkl['data'][n, :, :])
        data_pkl['data'][n, :, :] /= np.nanmedian(data_pkl['data'][n, :, :])

    return data_pkl


def rm_SAA(data_pkl, time_to_rm):

    args = np.where(data_pkl['SAA_time'] > time_to_rm)[0]
    data_pkl['data'] = data_pkl['data'][args, :, :]
    data_pkl['err'] = data_pkl['err'][args, :, :]
    data_pkl['SAA_time'] = data_pkl['SAA_time'][args]
    data_pkl['EXPEND'] = data_pkl['EXPEND'][args]

    return data_pkl


def make_input_fl(pix_num, data_pkl, exp_type, year):
    fl = dict()
    data = data_pkl['data']
    err = data_pkl['err']
    N_im, len_side, len_side = data.shape
    data = data.reshape(N_im, len_side*len_side)
    err = err.reshape(N_im, len_side*len_side)
    fl['pix_series'] = data[:, pix_num]
    fl['err_ext'] = err[:, pix_num]
    fl['pix_series'] = fl['pix_series'][~np.isnan(fl['pix_series'])]
    fl['err_ext'] = fl['err_ext'][~np.isnan(fl['pix_series'])]
    fl['N_im'] = len(fl['pix_series'])
    pickle.dump(fl, open('../data/%s/input_%s_%i.p' % (exp_type,
                                                       year,
                                                       pix_num), 'wb'))


if __name__ == '__main__':

    exp_type = sys.argv[1]
    year = sys.argv[2]
    file_location = sys.argv[3]
    if file_location == 'local':
        data_path = '../data/%s/' % exp_type
    else:
        data_path = '/Volumes/My_Book/wfc3_bad_pix/data/%s/' % exp_type
    data_path = data_path + '/data_%s_%s.p' % (exp_type, year)

    data_pkl = pickle.load(open(data_path, 'rb'))

    data_pkl = preprocess_data(data_pkl)

    data_pkl = rm_SAA(data_pkl, 3600)

    # num_pixels_to_make = 1000
    # np.random.seed(42)
    # pix_nums = np.random.randint(low=0,
    #                              high=1014*1014,
    #                              size=num_pixels_to_make)
    pix_nums = range(1014*1014)
    for pix_num in pix_nums:
        make_input_fl(pix_num, data_pkl, exp_type, year)
