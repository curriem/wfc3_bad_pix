import glob
import astropy.io.fits as pyfits
import numpy as np
import matplotlib.pyplot as plt
import sys

book_path = '/Volumes/My_Book/wfc3_bad_pix/data/'


def load_im(im_path):

    with pyfits.open(im_path, memmap=False) as im:
        data = im[1].data
        date = im[0].header['EXPEND']

    return data, date


def make_data_cubes(year):


    im_paths = glob.glob('/Volumes/My_Book/wfc3_bad_pix/data/set_%s/*' % year)
    dates = []
    data_cube = []
    for im_path in im_paths:
        data, date = load_im(im_path)
        data = pyfits.getdata(im_path, ext=1, memmap=False)
        date = pyfits.getval(im_path, 'EXPEND')
        dates.append(np.copy(date))
        data_cube.append(np.copy(data))
        del date
        del data

    dates = np.array(dates)
    data_cube = np.array(data_cube)
    sorted_args = np.argsort(dates)
    dates = dates[sorted_args]
    data_cube = data_cube[sorted_args, :, :]

    num_ims, num_x, num_y = data_cube.shape

    for x in range(1, num_x):
        for y in range(1, num_y):
            med_val = np.median(data_cube[:, x, y])
            data_cube[:, x, y] -= med_val
    np.save(book_path + '/data_cube_%s.npy' % year, data_cube)
    np.save(book_path + '/dates_%s.npy' % year, dates)


def bad_pix_cubes(year):

    mask = np.array([[1, 1, 1],
                     [1, 0, 1],
                     [1, 1, 1]], dtype=np.bool)

    data_cube = np.load('../data/data_cube_%s.npy' % year)
    num_ims, num_x, num_y = data_cube.shape
    bad_pix_cube = np.zeros_like(data_cube)

    for im in range(num_ims):
        print im
        for x in range(1, num_x-1):
            for y in range(1, num_y-1):
                stamp = data_cube[im, x-1:x+2, y-1:y+2]
                neighbors = stamp[mask]
                pix = stamp[~mask][0]
                val = (pix - np.mean(neighbors)) / np.std(neighbors)
                if np.abs(val) > 5:
                    bad_pix_cube[im, x, y] = 1

    np.save(book_path + '/bad_pix_cube_%s.npy' % year, bad_pix_cube)

def plot_maps(year):
    dates = np.load(book_path + '/dates_%s.npy' % year)
    bad_pix_cube = np.load(book_path + '/bad_pix_cube_%s.npy' % year)
    map = np.sum(bad_pix_cube, axis=0)

    map /= len(dates)
    print map.shape

    plt.figure()
    plt.imshow(map, origin='lower', cmap='jet')
    plt.colorbar()
    plt.axis('off')
    plt.savefig('../plots/frac_map_%s.pdf' % year)

    bins = np.arange(0.1, 1, 0.1)
    plt.figure()
    plt.hist(map.flatten(), bins=bins)
    plt.savefig('../plots/hist_%s.pdf' % year)
    '''
    plt.figure()
    plt.imshow(map2, origin='lower', cmap='gray')
    plt.colorbar()
    plt.axis('off')
    plt.savefig('../plots/flag_map_%s.pdf' % year)
    '''


if __name__ == '__main__':
    year = sys.argv[1]

    #make_data_cubes(year)
    bad_pix_cubes(year)
    #plot_maps(year)

