# -*- coding: utf-8 -*-

import sys

# Define constants
XLE_WEB_URL = "http://clarino.uib.no/iness/xle-web"

# def __main__():
# Read arguments
inp = sys.argv[1]
grammar = sys.argv[2]
text = open(inp, 'r').read()

outp = sys.argv[3]

# Define Indonesian as pre-selected grammar
data="""
<div>
    <p>To parse the text, press submit below. This will send your text to XLE-Web and
    open a new window with the parse results.</p>
    
    <form id='xle-web-form' action='##_XLE_WEB_URL_##' target='xle-web-frame' method='POST' style='display:none'>
        <input type='hidden' name='grammar' value='##_GRAMMAR_##'/>
        <input type='text' name='sentence' value="##_SENTENCE_##"/>
        <input type='hidden' name="parse-sentence" value="Parse sentence">
        <input type='submit'>
    </form>
</div>
"""

grammar = grammar.replace('__aring__', 'å')

data = data.replace('##_XLE_WEB_URL_##', XLE_WEB_URL)
data = data.replace('##_GRAMMAR_##', grammar)
data = data.replace('##_SENTENCE_##', text.replace('"', '&quot;'))

# write result in the output file
o = open(outp,'w')
o.write(data)
o.close()

# if __name__=="__main__": __main__()
