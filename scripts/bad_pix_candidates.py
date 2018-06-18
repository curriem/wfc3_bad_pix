import numpy as np
import matplotlib.pyplot as plt
import pickle
import make_inputs as mi


def get_rms_val(pix_series, uncertainty):

    val = (pix_series - np.mean(pix_series)) / np.sqrt(uncertainty**2
                                                       + 0.02**2)

    val = np.sqrt(np.sum(val**2) / len(val))

    return val


def plot_things(x_thing, y_thing):

    plt.figure()
    plt.scatter(x_thing, y_thing)
    plt.xlabel('rms value')
    plt.ylabel('outlier frac')
    plt.savefig('../plots/outfrac_rms.pdf')




if __name__ == '__main__':

    data_pkl = pickle.load(open('../data/darks/data_darks_2018a.p', 'rb'))

    data_pkl = mi.preprocess_data(data_pkl)

    data_pkl = mi.rm_SAA(data_pkl, 3600)

    num_pixels_to_make = 1000

    np.random.seed(42)
    pix_nums = np.random.randint(low=0,
                                 high=1014*1014,
                                 size=num_pixels_to_make)
    N_im, len_side, len_side = data_pkl['data'].shape
    data = data_pkl['data'].reshape(N_im, len_side*len_side)
    err = data_pkl['err'].reshape(N_im, len_side*len_side)

    rms_vals = []
    outlier_fracs = []
    for pix_num in pix_nums:
        rms_vals.append(get_rms_val(data[:, pix_num], err[:, pix_num]))
        output_pkl = pickle.load(open('../data/darks/output_2018a_%s.p'
                                      % pix_num, 'rb'))
        outlier_fracs.append(np.median(output_pkl['outlier_frac']))
    rms_vals = np.array(rms_vals)
    print len(np.where(rms_vals > 1.2)[0])
    print len(np.where(rms_vals > 1.5)[0])
    plot_things(rms_vals, outlier_fracs)

