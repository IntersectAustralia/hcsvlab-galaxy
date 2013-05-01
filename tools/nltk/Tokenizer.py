import sys
import os
import nltk
inp = sys.argv[1]
outp = sys.argv[2]
i = open(inp,'r').read()
o = open(outp,'w')
sents = nltk.sent_tokenize(i)
for sent in sents:
    words = nltk.word_tokenize(sent)
    for word in words:
        o.write(word)
        o.write('\n')
o.close()
