import pystan
import pickle
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Bad Pixel Model')
parser.add_argument('data_path', help='path to pickled data of wfc3 flats')
parser.add_argument('save_path', help='path to output txt file')
args = parser.parse_args()

model = """

data {
    int<lower=0> N_im; // number of images in data cube
    vector[N_im] pix_series;
    vector[N_im] err_ext;
}

parameters {
    real inlier_mean;
    real<lower=0, upper=1> outlier_frac;
    real<lower=0.05> sigma_outlier;
    real outlier_mean;
}


model {
    for (i in 1:N_im){
        target += log_sum_exp(log(1 - outlier_frac)
                              + normal_lpdf(pix_series[i] | inlier_mean,
                                                            sqrt(err_ext[i]^2 +
                                                                 0.02^2)),
                              log(outlier_frac)
                              + normal_lpdf(pix_series[i] | outlier_mean,
                                                            sigma_outlier));
    }
    inlier_mean ~ normal(0, 1);
    outlier_mean ~ normal(0, 1000);
    sigma_outlier ~ normal(0, 1000);
}

"""

sm = pystan.StanModel(model_code=model)

data_pkl = pickle.load(open(args.data_path, 'rb'))

N_im, N_pix = data_pkl['data'].shape

with open(args.save_path, 'w') as f:
    for n in range(N_pix):
        bad_fit = 1
        while bad_fit:
            fit = sm.sampling(data={'pix_series': data_pkl['data'][:, n],
                                    'err_ext': data_pkl['err'][:, n],
                                    'N_im': N_im},
                              iter=2000, chains=4, refresh=1000,
                              init=lambda: {'inlier_mean':
                                            np.median(data_pkl['data'][:, n]),
                                            'outlier_frac':
                                            np.random.random(),
                                            'sigma_outlier':
                                            np.clip(np.std(data_pkl['data'][:, n]),
                                                    0.05, 1e10),
                                            'outlier_mean':
                                            np.mean(data_pkl['data'][:, n])})

            str_fit = str(fit)
            parsed = str_fit.split('\n')

            for line in parsed:
                subparsed = line.split(None)
                if len(subparsed) > 2:
                    if subparsed[0] == "outlier_frac":
                        conv_r = float(subparsed[-1])
                        print "Found ", subparsed, conv_r
                        if conv_r < 1.05:
                            bad_fit = 0
                        else:
                            bad_fit = 1
                        print "bad_fit ", bad_fit

        la = fit.extract(permuted=True)

        for key in la.keys():
            f.write('\ndata  %s  pix  %i  x  %i  y  %i  '
                    % (args.data_path.split('/')[0], n,
                       data_pkl['x'][n], data_pkl['y'][n]))
            f.write('%s  %.5f  %.5f\n'
                    % (str(key), np.median(la[key]), np.std(la[key], ddof=1)))

        f.write(str_fit)
        f.flush()
