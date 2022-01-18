import pandas as pd
from gensim.models import Word2Vec
import string
import regex as re
import json
import numpy as np


# Filepaths
codenames_raw = '../data/raw_data/codenames_word_list.txt'
dictionary_raw = [
    '../data/raw_data/google-10000-english-usa-no-swears-long.txt',
    '../data/raw_data/google-10000-english-usa-no-swears-medium.txt',
    '../data/raw_data/google-10000-english-usa-no-swears-short.txt' 
]

codenames_output = '../data/processed_data/codenames_vecs_seg.json'
dictionary_output = '../data/processed_data/dictionary_vecs_seg.json'


# Process codenames word list
with open(codenames_raw) as f:
    raw_text = f.readlines()

codenames_word = set([x.strip().lower() for x in raw_text])


# Process dictionary corpus
processed_text = []
for file in dictionary_raw:
    with open(file) as f:
        raw_text = f.readlines()
        processed_text += [x.strip().lower() for x in raw_text]

dict_word = set(processed_text)


#process text corpus to train word2vec model
def parseData(filename):
    data = []
    for line in open(filename):
        l = line.lower()
        #all quality phrases
        qual_phrase = re.findall(r'(?:<phrase_q=\d\.[0-9]{3}>)(.*?)(?:</phrase>)', l) 
        qual_phrase_one_word = []
        #connect multi-word quality phrases with _
        for i in qual_phrase:
            qual_phrase_one_word.append(i.replace(' ', '_').replace('-', '_')) 
        #replace quality phrase with correct format
        final = re.sub(r'(?:<phrase_q=\d\.[0-9]{3}>)(.*?)(?:</phrase>)', lambda match: str(qual_phrase_one_word.pop(0)), l) 
        #replace punctuation with space
        final = re.sub(r'[\!\"\#\$\%\&\\\'\(\)\*\,\-\.\/\:\;\<\=\>\?\@\[\]\^\`\{\|\}\~]', ' ', final) 
        #replace muliple space with one space
        final = re.sub(r' +', ' ', final)
        #include phrases that have content
        if not bool(re.search('^ +$', final)) and len(final) != 0: 
            data.append(final.strip().split())
    return data


#parse document
data = parseData('../data/raw_data/autophrase_segmentation.txt')

#train word2vec model
model = Word2Vec(data, vector_size=300, window=5, min_count=1, workers=4)

#populate key-value pair (word:vector embeding)
codenames_vecs = {}
dictionary_vecs = {}
for i in model.wv.key_to_index:
    if i in codenames_word:
        codenames_vecs[i] = model.wv[i].tolist()
    elif i in dict_word:
        dictionary_vecs[i] = model.wv[i].tolist()


#output word vectors as key value pair in json
with open(codenames_output, 'w') as f:
    json.dump(codenames_vecs, f)

with open(dictionary_output, 'w') as f:
    json.dump(dictionary_vecs, f)

