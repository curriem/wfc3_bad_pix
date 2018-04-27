import commands

years = ['2009b',
         '2010a',
         '2010b',
         '2011a',
         '2011b',
         '2012a',
         '2012b',
         '2013a',
         '2013b',
         '2014a',
         '2014b',
         '2015a',
         '2015b',
         '2016a',
         '2016b',
         '2017b']

years1 = ['2014a', # 1.5 G
          '2016b', # 0.5 G
          '2010a', # 1.2 G
          '2010b', # 1.5 G
          '2011a', # 3.6 G
          '2012b', # 3.3 G
          '2013a', # 2.1 G
          '2009b'] # 1.0 G

years2 = ['2011b', # 1.8 G
          '2012a', # 3.6 G
          '2014b', # 1.5 G 
          '2015a', # 1.5 G
          '2017b', # 0.5 G
          '2013b', # 0.8 G
          '2015b', # 1.1 G
          '2016a'] # 4.0 G 

for year in years2:
    print 'python get_bad_pix.py %s' % year
    commands.getoutput('python get_bad_pix.py %s' % year)
