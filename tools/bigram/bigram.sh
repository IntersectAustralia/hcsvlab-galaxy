#!/bin/bash

# A basic bigram counting tool for text files.
#
# Usage:
# 
# ./bigram.sh input_file output_file
#
#   input_file: A plain text file
#   output_file: A tab-separated value file of bigram counts

# Translate non-character sequences to newlines
tr -sc '[A-Z][a-z]' '\n' < $1 > words.txt

# Copy this list, starting at the second line
tail -n +2 words.txt > nextwords.txt

# Paste these words side-by-side, sort them
paste words.txt nextwords.txt | sort > sorted_bigrams.txt

# Show only unique bigrams and their count, format the result as a tab separated value file
uniq -c sorted_bigrams.txt | awk '{printf("%s\t%s\t%s\n" , $1, $2, $3)}' > $2

# Remove the intermediate files
rm words.txt nextwords.txt sorted_bigrams.txt