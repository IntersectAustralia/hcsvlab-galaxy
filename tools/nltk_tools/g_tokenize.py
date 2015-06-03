import sys
import os
import nltk
import string
import argparse
import json
import codecs


def Parser():
  the_parser = argparse.ArgumentParser(description="tokenize a text")
  the_parser.add_argument('--input', required=True, action="store", type=str, help="input text file")
  the_parser.add_argument('--output', required=True,  action="store", type=str, help="output file path")
  the_parser.add_argument('--lower', required=False, action="store_true", help="lowercase all words")  
  the_parser.add_argument('--nopunct', required=False, action="store_true", help="remove all punctuation characters")
  args = the_parser.parse_args()
  return args

def readfile(file, access, encoding):
    with codecs.open(file, access, encoding) as f:
        return f.read()


# work
def tokenize(inp, outp, lower=False, nopunct=False):
    """Input: a text file
    Output: a tokenized version of the text, one token per line
    """    

    text = readfile(inp,'r','utf-8-sig')
    
    result = []
    sents = nltk.sent_tokenize(text)
    for sent in sents:
        
        if lower:
            words = [w.lower() for w in nltk.word_tokenize(sent)]
        else: 
            words = nltk.word_tokenize(sent)
        
        if nopunct:
            words = [w for w in words if not w in string.punctuation]
            
        result.append(words)

    # output

    o = open(outp,'w')
    o.write(json.dumps(result, indent=4))
    o.close()


if __name__=='__main__':

    args=Parser()
    
    tokenize(args.input, args.output, lower=args.lower, nopunct=args.nopunct)
    
    