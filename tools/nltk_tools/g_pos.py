import nltk
import argparse
import json

def arguments():
  parser = argparse.ArgumentParser(description="tokenize a text")
  parser.add_argument('--input', required=True, action="store", type=str, help="input text file")
  parser.add_argument('--output', required=True,  action="store", type=str, help="output file path")
  args = parser.parse_args()
  return args
  

def postag(in_file, out_file):
    """Input: a text file with one token per line
    Output: a version of the text with Part of Speech tags written as word/TAG
    """
    json_string = unicode(open(in_file, 'r').read(), errors='ignore')
    sentences = json.loads(json_string)
    postags = []
    for sentence in sentences:
        postags.append(nltk.pos_tag(sentence))
    output = open(out_file, 'w')
    output.write(json.dumps(postags, indent=4))
    output.close()


if __name__ == '__main__':
    args = arguments()
    postag(args.input, args.output)
    
    