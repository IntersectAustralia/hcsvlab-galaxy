import sys
import os
import nltk
import string
import argparse
import json

def Parser():
  the_parser = argparse.ArgumentParser(description="tokenize a text")
  the_parser.add_argument('--input', required=True, action="store", type=str, help="input text file")
  the_parser.add_argument('--output', required=True,  action="store", type=str, help="output file path")
  args = the_parser.parse_args()
  return args
  

# work
def postag(inp, outp):
    """Input: a text file with one token per line
    Output: a version of the text with Part of Speech tags written as word/TAG
    """    
    sentences = json.load(open(inp,'r'))
    
    postags = []
    for sent in sentences:
        postags.append(nltk.pos_tag(sent))
    
    # output
    o = open(outp,'w')
    o.write(json.dumps(postags, indent=4))
    o.close()


if __name__=='__main__':

    args=Parser()
    
    postag(args.input, args.output)
    
    