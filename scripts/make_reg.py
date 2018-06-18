with open('bad_pix_miles.reg', 'wb') as f:
    f.write('# Region file format: DS9 version 4.1\n')
    f.write('global color=green dashlist=8 3 width=1 '
            + 'font="helvetica 10 normal" select=1 highlite=1 dash=0 '
            + 'fixed=0 edit=1 move=1 delete=1 include=1 source=1\n')
    f.write('image\n')
    with open('../data/bad_pix_2014_new.txt', 'rb') as bad_new:
        for line in bad_new:
            line = line.strip('\n')
            coords = line.split(None)
            x, y = coords
            f.write('box(%s, %s, 1, 1, 0)\n' % (x, y))

with open('bad_pix_david.reg', 'wb') as f:
    f.write('# Region file format: DS9 version 4.1\n')
    f.write('global color=blue dashlist=8 3 width=1 '
            + 'font="helvetica 10 normal" select=1 highlite=1 dash=0 '
            + 'fixed=0 edit=1 move=1 delete=1 include=1 source=1\n')
    f.write('image\n')
    with open('/Users/mcurrie/GitRepos/step_1/bad_pix_list_wfc3.txt', 'rb') as bad_old:
        for line in bad_old:
            line = line.strip('\n')
            coords = line.split(None)
            x, y = coords
            f.write('box(%s, %s, 1, 1, 0)\n' % (x, y))
