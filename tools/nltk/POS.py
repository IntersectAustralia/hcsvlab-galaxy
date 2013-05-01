import sys
import os
import nltk
inp = sys.argv[1]
outp = sys.argv[2]
i = open(inp,'r')
o = open(outp,'w')
for line in i:
    sents = nltk.sent_tokenize(line)
    for sent in sents:
        words = nltk.word_tokenize(sent)
        pos = nltk.pos_tag(words)
        for tag in pos:
            o.write(tag[0] + '/' + tag[1] + ' ')
    o.write('\n')
o.close()
