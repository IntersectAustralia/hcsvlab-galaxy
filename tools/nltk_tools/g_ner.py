import sys
import os
import nltk
import string
import argparse
import json

def Parser():
  the_parser = argparse.ArgumentParser(description="run NER on a text")
  the_parser.add_argument('--input', required=True, action="store", type=str, help="input text file")
  the_parser.add_argument('--output', required=True,  action="store", type=str, help="output file path")
  args = the_parser.parse_args()
  return args
  

# work
def postag(inp, outp):
    """Input: a JSON formatted set of POS tags
    Output: a list of named entities found in the text
    """    
    # NER types
    tags = ['LOCATION', 'ORGANIZATION', 'PERSON', 'DURATION', 'DATE', 'CARDINAL', 'PERCENT', 'MONEY', 'MEASURE']
    
    sentences = json.load(open(inp,'r'))
    
    ner = []
    for sent in sentences:
        tree = nltk.ne_chunk(sent)
        for chunk in tree.subtrees(filter=lambda t: t.label() in tags):
            tag = chunk.label()
            phrase = ' '.join([x[0] for x in chunk.leaves()])
            ner.append(phrase + '\t' + tag)
            print phrase + '\t' + tag
        
    
    # output
    o = open(outp,'w')
    for row in ner:
        o.write(row + '\n')
    o.close()


if __name__=='__main__':

    args=Parser()
    
    postag(args.input, args.output)
    
    