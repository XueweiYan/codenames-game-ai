from bs4 import BeautifulSoup
import lxml
from gensim.models import Word2Vec
import string
import json


# Filepaths
codenames_raw = '../data/raw_data/codenames_word_list.txt'
dictionary_raw = '../data/raw_data/enwiki-20190320-words-frequency.txt'

# Process codenames word list
with open(codenames_raw) as f:
    raw_text = f.readlines()

codenames_word = set([x.strip().lower() for x in raw_text])


# Process dictionary corpus and separate by size
with open(dictionary_raw) as f:
    word_10k = [next(f) for x in range(10000)]
    word_20k = [next(f) for x in range(10000)]
    word_30k = [next(f) for x in range(10000)]

dict_word_10k = set([x.strip().split()[0].lower() for x in word_10k])
dict_word_20k = set([x.strip().split()[0].lower() for x in word_20k])
dict_word_30k = set([x.strip().split()[0].lower() for x in word_30k])


#process text corpus to train word2vec model
def parseXML(filename):
    file = open(filename, 'r')
    soup = BeautifulSoup(file, 'lxml')
    data = []
    translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    for text in soup.find_all('text'):
        line = str(text).lower()
        #replace punctuation with space
        line = line.translate(translator) 
        #tokenize words
        words = line.strip().split()
        #stem words (find the root word)
        if len(words) != 0: 
            data.append(words)
    return data


#parse document
file = '../data/raw_data/simplewiki-20211001-pages-articles-multistream.xml'
data = parseXML(file)

#train word2vec model
model = Word2Vec(data, vector_size=300, window=5, min_count=1, workers=4)

#populate key-value pair (word:vector embeding)
codenames_vecs = {}
dictionary_vecs_10k = {}
dictionary_vecs_20k = {}
dictionary_vecs_30k = {}

for i in model.wv.key_to_index:
    if i in codenames_word:
        codenames_vecs[i] = model.wv[i].tolist()
    elif i in dict_word_10k:
        dictionary_vecs_10k[i] = model.wv[i].tolist()
    elif i in dict_word_20k:
        dictionary_vecs_20k[i] = model.wv[i].tolist()
    elif i in dict_word_30k:
        dictionary_vecs_30k[i] = model.wv[i].tolist()

codenames_output = '../data/processed_data/codenames_vecs_wiki.json'
dictionary_output_10k = '../data/processed_data/dictionary_vecs_wiki_10k.json'
dictionary_output_20k = '../data/processed_data/dictionary_vecs_wiki_20k.json'
dictionary_output_30k = '../data/processed_data/dictionary_vecs_wiki_30k.json'
dict_files = [dictionary_output_10k, dictionary_output_20k, dictionary_output_30k]
dict_vecs = [dictionary_vecs_10k, 
            {**dictionary_vecs_10k, **dictionary_vecs_20k},
            {**dictionary_vecs_10k, **dictionary_vecs_20k, **dictionary_vecs_30k}]


#output word vectors as key value pair in json
with open(codenames_output, 'w') as f:
    json.dump(codenames_vecs, f)

for i in range(3):
    with open(dict_files[i], 'w') as f:
        json.dump(dict_vecs[i], f)
