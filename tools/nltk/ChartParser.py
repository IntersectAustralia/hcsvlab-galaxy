import sys
import os
import nltk
from nltk.corpus import PlaintextCorpusReader
inp = sys.argv[1]
gram = sys.argv[2]
outp = sys.argv[3]
text = open(inp,'r').read()
o = open(outp,'w')
grammar_file = open(gram,'r').read()
try:
    grammar = nltk.parse_cfg(grammar_file)
    parser = nltk.ChartParser(grammar)

    sents = nltk.sent_tokenize(text)
    for sent in sents:
        words = nltk.word_tokenize(sent)
        tree = parser.parse(words)
        print >> o, tree
except Exception, e:
    import sys
    sys.stderr.write("Error with parsing. Check the input files are correct and the grammar contains every word in the input sequence. \n----\n" + str(e))
    sys.exit()
o.close()
