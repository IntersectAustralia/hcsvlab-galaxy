import sys
import os
import urllib2
file_list = sys.argv[1]
outp = sys.argv[2]
o = open(outp,'w')
file_list = file_list.replace('__tc__', '')
file_list = file_list.replace(' ', '')
files = file_list.split("__cn__")
for f in files:
    try:
        content = urllib2.urlopen(f)
        stri = unicode(content.read(), errors='ignore')
        o.write(stri)
        o.write('\n')
    except:
        pass
o.close
