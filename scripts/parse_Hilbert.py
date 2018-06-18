H_fl = '../data/Hilbert_badpix_files.txt'
raw_fl_list = []
flt_fl_list = []
with open(H_fl, 'rb') as f:
    for line in f:
        line = line.split(None)
        for item in line:
            item = item.strip(',')
            item = item.split('.')[0]
            dat, ext = item.split('_')
            if ext == 'raw':
                raw_fl_list.append(dat)
            elif ext == 'flt':
                flt_fl_list.append(dat)
            else:
                assert False

print raw_fl_list
print flt_fl_list

with open('../data/raw_Hilbert_fls.txt', 'wb') as f:
    for item in raw_fl_list:
        f.write('%s\n' % item)

with open('../data/flt_Hilbert_fls.txt', 'wb') as f:
    for item in flt_fl_list:
        f.write('%s\n' % item)
