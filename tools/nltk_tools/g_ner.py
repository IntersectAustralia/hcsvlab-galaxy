import nltk
import string
import argparse
import json


def arguments():
    parser = argparse.ArgumentParser(description="run NER on a text")
    parser.add_argument('--input', required=True, action="store", type=str, help="input text file")
    parser.add_argument('--output', required=True,  action="store", type=str, help="output file path")
    args = parser.parse_args()
    return args


def ner(in_file, out_file):
    """Input: a JSON formatted set of POS tags
    Output: a list of named entities found in the text
    """
    # NER types
    tags = ['LOCATION', 'ORGANIZATION', 'PERSON', 'DURATION',
            'DATE', 'CARDINAL', 'PERCENT', 'MONEY', 'MEASURE']

    json_string = unicode(open(in_file, 'r').read(), errors='ignore')
    sentences = json.loads(json_string)
    ner = []
    for sentence in sentences:
        tree = nltk.ne_chunk(sentence)
        for chunk in tree.subtrees(filter=lambda t: t.label() in tags):
            tag = chunk.label()
            phrase = ' '.join([x[0] for x in chunk.leaves()])
            ner.append(phrase + '\t' + tag)
            print phrase + '\t' + tag

    output = open(out_file, 'w')
    for row in ner:
        output.write(row)
        output.write('\n')
    output.close()


if __name__ == '__main__':
    args = arguments()
    ner(args.input, args.output)
