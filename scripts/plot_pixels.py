import sys
import glob
import cPickle as pickle
import numpy as np
import matplotlib.pyplot as plt


def plot_hist(vals, title):
    plt.figure()
    plt.hist(vals)
    plt.title(title)
    plt.savefig('../plots/hist_'+title+'.pdf')


def plot_scatter(vals, labels, title):
    plt.figure(figsize=(15, 9))
    for n in range(len(vals)):
        plt.scatter(n, vals[n])
        plt.text(n, vals[n], coords_calculator(int(labels[n])))
    plt.title(title)
    plt.savefig('../plots/scatter_'+title+'.pdf')


def coords_calculator(pix_num):

    map = np.zeros((1014, 1014))
    map = map.flatten()
    map[pix_num] = 1
    map = map.reshape((1014, 1014))
    i, j = np.where(map == 1)
    x = j[0]+1
    y = i[0]+1

    return x, y


def plot_input(outlier_fracs, pix_nums, SAA_time, exp_type, year):
    for n in range(len(outlier_fracs))[:10]:
        input_path = '../data/%s/input_%s_%s.p' % (exp_type,
                                                   year,
                                                   pix_nums[n])
        input_data = pickle.load(open(input_path, 'rb'))
        pix_series = input_data['pix_series']
        err = input_data['err_ext']

        plt.figure()
        plt.errorbar(SAA_time[np.where(SAA_time > 3600)[0]],
                     pix_series, yerr=err, fmt='o')
        plt.title(str(pix_nums[n]) + ' ' + str(outlier_fracs[n]))
        plt.savefig('../plots/series_%s_%s.pdf' % (exp_type, str(pix_nums[n])))


if __name__ == '__main__':
    exp_type = sys.argv[1]
    year = sys.argv[2]
    output_pkls = glob.glob('../data/%s/output_%s*.p' % (exp_type, year))
    data_pkl = pickle.load(open('../data/%s/data_%s_%s.p' % (exp_type,
                                                             exp_type,
                                                             year), 'rb'))
    SAA_time = data_pkl['SAA_time']
    outlier_fracs = []
    inlier_means = []
    sigma_outliers = []
    outlier_means = []
    pix_nums = []
    for output_path in output_pkls:
        output = pickle.load(open(output_path, 'rb'))
        pix_num = output_path.split('_')[-1].strip('.npy')
        pix_nums.append(pix_num)
        outlier_fracs.append(np.median(output['outlier_frac']))
        inlier_means.append(np.median(output['inlier_mean']))
        sigma_outliers.append(np.median(output['sigma_outlier']))
        outlier_means.append(np.median(output['outlier_mean']))

    plot_hist(outlier_fracs, exp_type)
    plot_scatter(outlier_fracs, pix_nums, exp_type)
    plot_input(outlier_fracs, pix_nums, SAA_time, exp_type, year)
