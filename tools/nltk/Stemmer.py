import sys
import os
import nltk
from nltk.stem import *
inp = sys.argv[1]
outp = sys.argv[2]
stemmer = sys.argv[3]
i = open(inp,'r').read()
o = open(outp,'w')
sents = nltk.sent_tokenize(i)
for sent in sents:
    words = nltk.word_tokenize(sent)
    if stemmer == 'snowball':
        st = snowball.EnglishStemmer()
    if stemmer == 'lancaster':
        st = LancasterStemmer()
    if stemmer == 'porter':
        st = PorterStemmer()
    else:
        st = snowball.EnglishStemmer()
    for item in words:
        s = st.stem(item)
        o.write(s)
        o.write('\n')
o.close()
