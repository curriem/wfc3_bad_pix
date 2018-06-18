import glob
import sys
import matplotlib.pyplot as plt
import numpy as np
import pyfits

def make_reg_fl(x, y, outlier_fracs, year):
    with open('%s_stan_pixels.reg' % year, 'wb') as f:
        f.write('# Region file format: DS9 version 4.1\n')
        f.write('global color=green dashlist=8 3 width=1 '
                + 'font="helvetica 10 normal" select=1 highlite=1 dash=0 '
                + 'fixed=0 edit=1 move=1 delete=1 include=1 source=1\n')
        f.write('image\n')
        for n in range(len(x)):
            if outlier_fracs[n] < 0.03:
                color = 'magenta'
            elif 0.03 <= outlier_fracs[n] < 0.1:
                color = 'green'
            elif 0.1 <= outlier_fracs[n] < 0.3:
                color = 'cyan'
            elif 0.3 <= outlier_fracs[n] < 0.5:
                color = 'blue'
            elif 0.5 <= outlier_fracs[n] < 0.7:
                color = 'yellow'
            elif 0.7 <= outlier_fracs[n] < 0.9:
                color = 'orange'
            elif 0.8 <= outlier_fracs[n] <= 1.0:
                color = 'red'
            '''
            elif 0.5 <= outlier_fracs[n] < 0.6:
                color = '#c6e2ff' # light blue
            elif 0.6 <= outlier_fracs[n] < 0.7:
                color = '#ffff00' # yellow 
            elif 0.7 <= outlier_fracs[n] < 0.8:
                color = '#ffa500' # orange
            else:
                color = '#ff0000' # red
            '''
            if (outlier_fracs[n] > 0.1):
                f.write('box(%s, %s, 1, 1, 0) # color=%s fill=0.5\n'
                        % (x[n], y[n], color))


def make_hist(outlier_fracs, year):
    plt.figure()
    plt.hist(outlier_fracs, bins=np.arange(0.1, 1.05, 0.05),
             label='erratic pixels')
    n, b, p = plt.hist(outlier_fracs, bins=np.arange(0.1, 1.05, 0.05),
                       weights=outlier_fracs,
                       label='erratic pixels, weighted by outlier fraction')
    plt.xlabel('Outlier Fraction')
    plt.ylabel('Number per bin')
    plt.axhline(np.median(n), color='k', label='median of weighted bins')
    plt.legend()
    plt.tight_layout()
    plt.savefig('../plots/%s_bad_pix_hist.pdf' % year, bbox_inches='tight')


def make_scatter_new(outlier_fracs, sig_outlier, year):
    plt.figure()
    plt.scatter(sig_outlier, outlier_fracs)
    plt.xlabel('sig_outlier')
    plt.ylabel('outlier_fracs')


def make_scatter(x, y, outlier_fracs, year):
    plt.figure()
    map = np.empty((1014, 1014))
    map[y, x] = outlier_fracs
    plt.imshow(map, origin='lower')
    plt.colorbar()
    plt.axis('off')
    plt.show()
    #cm = plt.scatter(x, y, c=outlier_fracs, s=1)
    #plt.colorbar(cm)
    #plt.xlabel('x')
    #plt.ylabel('y')
    #plt.show()

#    plt.figure()
#    plt.scatter(range(len(outlier_fracs)), outlier_fracs)
#    plt.ylabel('outlier fracs')
#    plt.show()


def binned_colors(outlier_fracs):
    colors = ['none',      # 0-0.1
              'limegreen', # 0.1-0.3
              'cyan',      # 0.3-0.5
              'yellow',    # 0.5-0.7
              'orange',    # 0.7-0.9
              'red']       # 0.9-1.0
    bins = [0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0]
    labels = []
    grn_label = 1
    cyan_label = 1
    ylw_label = 1
    orng_label = 1
    red_label = 1

    digitized = np.digitize(outlier_fracs, bins)
    plotting_colors = []
    for item in digitized:
        plotting_colors.append(colors[item-1])

    labels = []
    for color in plotting_colors:
        if grn_label and color == 'green':
            labels.append('0.1-0.3')
            grn_label = 0
        elif cyan_label and color == 'cyan':
            labels.append('0.3-0.5')
            cyan_label = 0
        elif ylw_label and color == 'yellow':
            labels.append('0.5-0.7')
            ylw_label = 0
        elif orng_label and color == 'orange':
            labels.append('0.7-0.9')
            orng_label = 0
        elif red_label and color == 'red':
            labels.append('>0.9')
            red_label = 0
        else:
            labels.append('_nolegend_')
    return plotting_colors, labels

def plot_image(x_im, y_im, outlier_fracs, impath, year, H_orig):
    size = 50
    xstart = 75
    ystart = 800

    im = pyfits.getdata(impath, 1)
    im_outlfrac = np.empty_like(im)
    plotting_x = []
    plotting_y = []
    plotting_outlfrac = []
    plotting_xH = []
    plotting_yH = []
    plotting_H = []
    for n in range(len(x_im)):
        im_outlfrac[x_im[n]-1, y_im[n]-1] = outlier_fracs[n]
    data = im[ystart-1:ystart-1 + size, xstart-1:xstart-1 + size]
    data_outlfrac = im_outlfrac[ystart-1:ystart-1 + size, xstart-1:xstart-1 +
                                size]
    C_orig = np.load('../data/C_bad_pix_map.npy')
    H_orig = H_orig[ystart-1:ystart-1 + size, xstart-1:xstart-1 +size]
    plt_x_len, plt_y_len = data_outlfrac.shape
    for x in range(plt_x_len):
        for y in range(plt_y_len):
            if data_outlfrac[x, y] > 0.1:
                print x+ystart, y+xstart
                plotting_x.append(x)
                plotting_y.append(y)
                plotting_outlfrac.append(data_outlfrac[x, y])
    for x in range(plt_x_len):
        for y in range(plt_y_len):
            if H_orig[x, y]:
                plotting_xH.append(x)
                plotting_yH.append(y)
                plotting_H.append(H_orig[x, y])
    data = np.clip(data, -0.5, 2)
    fig, axes = plt.subplots(2, 1, figsize=(5, 7))

    print data.shape
    axes[0].imshow(data, origin='lower', cmap='gray',
               interpolation='nearest')
    axes[0].scatter(plotting_x, plotting_y,
                     marker='s', facecolors='none',
                     s=6,
                     edgecolors='r',
                     #edgecolors=binned_colors(plotting_outlfrac)[0],
                     #label=binned_colors(plotting_outlfrac)[1],
                     linewidth=0.5)
    axes[0].axis('off')


    axes[1].imshow(data, origin='lower', cmap='gray',
                   interpolation='nearest')
    '''
    axes[1].scatter(plotting_xH, plotting_yH,
                    marker='s', facecolors='none',
                    s=6,
                    edgecolors='r',
                    linewidth=0.5)
    '''
    axes[1].axis('off')
    axes[0].set_title('Hilbert 2012')
    axes[1].set_title('Currie 2018')
    #plt.axes().set_aspect('equal', 'datalim')

    plt.tight_layout()

    plt.savefig('../plots/%s_bad_pix_im.pdf' % year, bbox_inches='tight',
                pad_inches=0)
    plt.show()

def get_pix_counts(outlier_frac):
    bins = [0, 0.03, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6,
            0.7, 0.8, 0.9, 1.]
    bin_idx = np.digitize(outlier_frac, bins)
    print np.bincount(bin_idx)



def make_bad_pix_map(x, y, outlier_fracs, year):
    C_bad_pix_map = np.zeros((1014, 1014), dtype=bool)

    outlier_fracs = np.array(outlier_fracs)
    greater_10_inds = np.where(outlier_fracs > 0.1)
    print greater_10_inds
    vals = np.zeros_like(outlier_fracs, dtype=bool)
    print vals
    vals[greater_10_inds] = 1
    print vals

    C_bad_pix_map[y-1, x-1] = vals
    plt.figure()
    plt.imshow(C_bad_pix_map, origin='lower')
    plt.show()
    np.save('../data/%s_bad_pix_map.npy' % year, C_bad_pix_map)

year = sys.argv[1]

output_fls = glob.glob('../data/output_%s*' % year)

x = []
y = []
outlier_fracs = []
sigma_outliers = []
inlier_mean_unc = []
for output_fl in output_fls:
    with open(output_fl, 'rb') as f:
        for line in f:
            line = line.split(None)
            if len(line) == 11:
                if line[8] == 'outlier_frac':
                    x.append(int(line[5]))
                    y.append(int(line[7]))
                    outlier_fracs.append(float(line[9]))
                if line[8] == 'sigma_outlier':
                    sigma_outliers.append(float(line[9]))
                if line[8] == 'inlier_mean':
                    inlier_mean_unc.append(float(line[10]))
            else:
                pass
x = np.array(x)
y = np.array(y)

H_orig = np.load('../data/H_bad_pix_map.npy')

#make_hist(outlier_fracs, year)
#plot_image(x, y, outlier_fracs, './Hilbert_2012im1.fits', year, H_orig)
make_bad_pix_map(x, y, outlier_fracs, year)
#make_reg_fl(x, y, outlier_fracs, year)
