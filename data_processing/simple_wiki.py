from bs4 import BeautifulSoup
import lxml
import pandas as pd
from gensim.models import Word2Vec
import json
import numpy as np
import regex as re


# Filepaths
codenames_raw = '../data/raw_data/codenames_word_list.txt'
dictionary_raw = [
    '../data/raw_data/google-10000-english-usa-no-swears-long.txt',
    '../data/raw_data/google-10000-english-usa-no-swears-medium.txt',
    '../data/raw_data/google-10000-english-usa-no-swears-short.txt']

codenames_output = '../data/processed_data/codenames_vecs_wiki.json'
dictionary_output = '../data/processed_data/dictionary_vecs_wiki.json'


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
def parseXML(filename):
    file = open(filename, 'r')
    soup = BeautifulSoup(file, 'lxml')
    data = []
    for text in soup.find_all('text'):
        text = str(text).lower()
        #replace punctuation with space
        text = re.sub(r'[\!\"\#\$\%\&\\\'\(\)\*\,\-\.\/\:\;\<\=\>\?\@\[\]\^\`\{\|\}\~]', ' ', text) 
        #replace muliple space with one space
        text = re.sub(r' +', ' ', text)
        #include phrases that have content
        if not bool(re.search('^ +$', text)) and len(text) != 0: 
            data.append(text.strip().split())
    return data


#parse document
file = '../data/raw_data/simplewiki-20211001-pages-articles-multistream.xml'
data = parseXML(file)

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

