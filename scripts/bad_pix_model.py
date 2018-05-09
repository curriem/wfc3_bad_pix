import pystan
import pickle
import numpy as np
import sys

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

data_num = sys.argv[1]

data_path = '../data/input_2017_%s.p' % data_num

data_pkl = pickle.load(open(data_path, 'rb'))

N_im, N_pix = data_pkl['data'].shape

save_path = '../data/output_2017_%s.txt' % data_num

with open(save_path, 'a') as f:
    for n in range(len(N_pix)):
        fit = sm.sampling(data={'pix_series': data_pkl['data'][: n],
                                'err_ext': data_pkl['err'][:, n],
                                'N_im': N_im},
                          iter=2000, chains=4,
                          init={'inlier_mean':
                                np.median(data_pkl['data'][: n]),
                                'outlier_frac': np.random.random(),
                                'sigma_outlier':
                                np.clip(np.std(data_pkl['data'][: n]),
                                        0.05, 1e10),
                                'outlier_mean':
                                np.mean(data_pkl['data'][: n])})

        la = fit.extract(permuted=True)
        for key in la.keys():
            la[key] = np.median(la[key])
            f.write('data %i pix %i ' % (data_num, n))
            f.write('%s\t%0.5fi\n' % (str(key), la[key]))
            str_fit = str(fit)
            f.write(str_fit)
            f.flush()
