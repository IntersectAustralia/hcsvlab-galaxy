import sys
import os
import nltk
from nltk.corpus import PlaintextCorpusReader

def print_out(text, sentences):
    outp = sys.argv[2]
    o = open(outp,'w')
    curr = 0
    for sent in sentences:
        times = count_occurences(sent, sent[-1])
        curr = text.find(sent[0], curr)
        end = find_nth(text, sent[-1], times, curr) + len(sent[-1])
        o.write(text[curr:end] + '\n')
        curr = end
    o.close()

def find_nth(string, sub, n, offset):
    start = string.find(sub, offset)
    while start >= 0 and n > 1:
        start = string.find(sub, start+len(sub))
        n -= 1
    return start

def count_occurences(lst, string):
    count = 0
    for item in lst:
        if string in item:
            count += 1
    return count

inp = sys.argv[1]
i = open(inp,'r').read()
corpus = PlaintextCorpusReader(os.path.dirname(inp),os.path.basename(inp))
sents = corpus.sents()
print_out(i, sents)

