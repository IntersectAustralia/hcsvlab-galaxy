import sys
import pycurl
import cStringIO

file_list = sys.argv[1]
api_key = sys.argv[2]
outp = sys.argv[3]
o = open(outp, 'w')
files = file_list.split(",")
for f in files:
    try:
        curl = pycurl.Curl()
        buf = cStringIO.StringIO()
        curl.setopt(curl.URL, f)
        curl.setopt(pycurl.HTTPHEADER, ['X-API-KEY: ' + api_key, 'Accept: application/json'])
        curl.setopt(curl.WRITEFUNCTION, buf.write)
        curl.perform()
        string = buf.getvalue()
        if curl.getinfo(pycurl.HTTP_CODE) == 200:
            o.write(string)
            o.write('\n')
        buf.close()
    except:
        pass
o.close
