import sys
import os
import nltk
from nltk import FreqDist
inp = sys.argv[1]
outp = sys.argv[2]
pos = bool(sys.argv[3] == 'true')
i = open(inp,'r').read()
o = open(outp,'w')
if pos:
    text = i.split(' ')[:-1]
    all_words = [x[0:x.index('/')] if x != '\n' else x for x in text]
    all_words = [x.lower().strip(' ').strip('\n') for x in all_words]
else:
    sents = nltk.sent_tokenize(i)
    all_words = []
    for sent in sents:
        words = nltk.word_tokenize(sent)
        all_words += words
    all_words = [x.lower() for x in all_words]
freq = FreqDist(all_words)
for word in freq.keys():
    o.write(word)
    o.write('\t\t\t' + str(freq[word]))
    o.write('\n')
o.close()
