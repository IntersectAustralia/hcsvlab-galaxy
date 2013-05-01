import sys
import os
import nltk
from nltk.collocations import *
inp = sys.argv[1]
outp = sys.argv[2]
freq_filter = sys.argv[3]
results = sys.argv[4]
coll_type = sys.argv[5]
pos = bool(sys.argv[6] == 'true')
i = open(inp,'r').read()
o = open(outp,'w')
all_words = []
if pos:
    text = i.split(' ')[:-1]
    all_words = [x[0:x.index('/')] if x != '\n' else x for x in text]
    all_words = [x.strip(' ').strip('\n') for x in all_words]
else:
    sents = nltk.sent_tokenize(i)
    for sent in sents:
        all_words += nltk.word_tokenize(sent)
if coll_type == 'bigram':
    measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(all_words)
else:
    measures = nltk.collocations.TrigramAssocMeasures()
    finder = TrigramCollocationFinder.from_words(all_words)
finder.apply_freq_filter(int(freq_filter))
colls = finder.nbest(measures.pmi, int(results))
for coll in colls:
    o.write(str(coll))
    o.write('\n')
o.close()
