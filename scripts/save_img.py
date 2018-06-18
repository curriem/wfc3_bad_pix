import numpy as np
import pyfits
import commands
import pickle
import sys

dat = sys.argv[1]
imname = sys.argv[2]

def save_img(dat, imname):

    commands.getoutput("rm -f " + imname)
    fitsobj = pyfits.HDUList()
    hdu = pyfits.PrimaryHDU()
    hdu.data = dat
    fitsobj.append(hdu)
    fitsobj.writeto(imname)
    fitsobj.close()


data = np.load(dat)
data = data[:500, :, :, 0]
save_img(data, imname)


