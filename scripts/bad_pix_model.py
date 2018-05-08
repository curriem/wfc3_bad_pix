import pystan
import pickle
import numpy as np
import sys
import glob

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


def initfn():
    return dict(inlier_mean=np.median(input_fl["pix_series"]),
                outlier_frac=np.random.random(),
                sigma_outlier=np.clip(np.std(input_fl["pix_series"]),
                                      0.05, 1e10),
                outlier_mean=np.mean(input_fl["pix_series"]))

sm = pystan.StanModel(model_code=model)

exp_type = sys.argv[1]
year = sys.argv[2]

input_fls = glob.glob('../data/%s/input*%s*' % (exp_type, year))

for input_fl in input_fls:
    pix_num = input_fl.split('_')[-1].strip('.p')

    input_fl = pickle.load(open(input_fl, 'rb'))

    save_path = '../data/%s/output_%s_%s.p' % (exp_type, year, pix_num)
    save_fit_path = '../data/%s/output_%s_%s.txt' % (exp_type, year, pix_num)

    fit = sm.sampling(data=input_fl, iter=2000, chains=4, init=initfn)

    la = fit.extract(permuted=True)
    pickle.dump(la, open(save_path, 'w'))
    str_fit = str(fit)
    with open(save_fit_path, 'wb') as f:
        f.write(str_fit)
        f.flush()
