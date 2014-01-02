import sys
import os
import urllib

# Define constants
XLE_WEB_URL = "http://clarino.uib.no/iness/xle-web"

# Read arguments
inp = sys.argv[1]
text = open(inp,'r').read()

outp = sys.argv[2]

# Define Indinesian as pre-selected grammar
params = urllib.urlencode({'grammar': 'Indonesian', 'sentence': text})
data="<div width='100%' height='100%'><iframe src='" + XLE_WEB_URL + "?" + params + "' width='100%' height='100%' frameborder='0'></iframe></div>"

# write result in the output file
o = open(outp,'w')
o.write(data)
o.close()
