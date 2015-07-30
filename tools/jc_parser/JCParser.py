import sys
import os
import nltk
import jcp.johnsoncharniak
from nltk.draw.util import CanvasFrame
from nltk.draw import TreeWidget
from subprocess import call
inp = sys.argv[1]
outp = sys.argv[2]
directory = sys.argv[3]
if not os.path.exists(directory): os.makedirs(directory)
from nltk.corpus import PlaintextCorpusReader
corpus = PlaintextCorpusReader(os.path.dirname(inp),os.path.basename(inp))
sents = corpus.sents()
parser = nltk.parse.JohnsonCharniak()

# Assumes X11 window is setup, with display variable :1
os.environ["DISPLAY"] = ":1"

links = "<h2><center><a href='combined.html'>Combined</a> | <a href='text.html'>Text Only</a> | <a href='drawing.html'>Drawing Only</a></center></h2><br>"

text = open((directory +'/text.html'),'w')
text.write('<style type="text/css"> p {font-family:monospace;} </style>\n')
text.write(links + "\n")
drawing = open((directory +'/drawing.html'),'w')
drawing.write('<style type="text/css"> img {max-width:100%;} </style>\n')
drawing.write(links + "<br>\n")

o = open(outp,'w')
o.write('<style type="text/css"> img {max-width:100%;} p {font-family:monospace;} </style>\n')
o.write(links)
o.write('<p>')
text.write('<p>')

for index, item in enumerate(sents):
	if len(item) == 1 and item[0] == ".":
		continue
	tree = parser.parse(item)
	o.write(tree.pprint().replace("\n", "<br>").replace("  ", "&nbsp;&nbsp;") + "\n")
	o.write("<br><br><br>\n")
	text.write(tree.pprint().replace("\n", "<br>").replace("  ", "&nbsp;&nbsp;") + "\n")
	text.write("<br><br><br>\n")
	cf = CanvasFrame(width=1200, height=1200, closeenough=1)
	tc = TreeWidget(cf.canvas(), tree, node_font=('helvetica',-18, 'bold'), leaf_font=('helvetica', -18, 'italic'), roof_fill='white', roof_color='black', 			leaf_color='green4', node_color='blue2')
	cf.add_widget(tc,10,10)
	os.chdir(directory)
	cf.print_to_file('tree.ps')
	call("convert -trim tree.ps tree" + str(index) + ".png", shell=True, stdout=open(os.devnull, 'wb'))
	o.write('<a href="tree' + str(index) + '.png" target="_blank"><img src="tree' + str(index) + '.png"/></a><br><br><br><br>\n')
	drawing.write('<a href="tree' + str(index) + '.png" target="_blank"><img src="tree' + str(index) + '.png"/></a><br><br><br><br>\n')

o.write("</p>")
text.write("</p>")
o.close()
text.close()
drawing.close()
combined = open((directory +'/combined.html'),'w')
combined.write(open(outp,'r').read())
combined.close()
