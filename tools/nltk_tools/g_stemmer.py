import sys
import os
import nltk
from nltk.stem import *
import argparse


def Parser():
    the_parser = argparse.ArgumentParser(description="Segments the text input into separate sentences")
    the_parser.add_argument('--input', required=True, action="store", type=str, help="input text file")
    the_parser.add_argument('--output', required=True, action="store", type=str, help="output file path")
    the_parser.add_argument('--stemmer', required=False, action="store", type=str, help="output file path")

    args = the_parser.parse_args()
    return args

def stemmer(inp, outp, stemmer):
    i = open(inp, 'r').read()
    o = open(outp, 'w')
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

if __name__ == '__main__':
    args = Parser()
    stemmer(args.input, args.output, args.stemmer)
