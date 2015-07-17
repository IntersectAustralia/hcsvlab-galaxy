import sys
import os
import nltk
import argparse
from nltk.corpus import PlaintextCorpusReader

def Parser():
  the_parser = argparse.ArgumentParser(description="run NER on a text")
  the_parser.add_argument('--input', required=True, action="store", type=str, help="input text file")
  the_parser.add_argument('--grammar', required=True,  action="store", type=str, help="grammar file")
  the_parser.add_argument('--output', required=True,  action="store", type=str, help="output file path")
  args = the_parser.parse_args()
  return args


def chart_parse(inp, gram, outp):

    text = open(inp, 'r').read()
    o = open(outp, 'w')
    grammar_file = open(gram, 'r').read()
    try:
        grammar = nltk.CFG.fromstring(grammar_file)
        parser = nltk.ChartParser(grammar)

        sents = nltk.sent_tokenize(text)
        for sent in sents:
            words = nltk.word_tokenize(sent)
            tree = parser.parse(words)
            print >> o, tree
    except Exception, e:
        import sys

        sys.stderr.write(
            "Error with parsing. Check the input files are correct and the grammar contains every word in the input sequence. \n----\n" + str(
                e))
        sys.exit()
    o.close()

if __name__=='__main__':

    args=Parser()

    chart_parse(args.input, args.grammar, args.output)


