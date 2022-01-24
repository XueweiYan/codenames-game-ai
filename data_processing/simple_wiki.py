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


dict_size = [3000, 5000, 10000, 20000, 30000]
dict_word = {}

# Process dictionary corpus and separate by size
for size in dict_size:
    with open(dictionary_raw) as f:
        dict_word[size] = set([next(f).strip().split()[0].lower() for x in range(size)])



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
dictionary_vecs = {3:{}, 5:{}, 10:{}, 20:{}, 30:{}}

for i in model.wv.key_to_index:
    if i in codenames_word:
        codenames_vecs[i] = model.wv[i].tolist()
    if i in dict_word[3000]:
        dictionary_vecs[3][i] = model.wv[i].tolist()
    if i in dict_word[5000]:
        dictionary_vecs[5][i] = model.wv[i].tolist()
    if i in dict_word[10000]:
        dictionary_vecs[10][i] = model.wv[i].tolist()
    if i in dict_word[20000]:
        dictionary_vecs[20][i] = model.wv[i].tolist()
    if i in dict_word[30000]:
        dictionary_vecs[30][i] = model.wv[i].tolist()

codenames_output = '../data/processed_data/codenames_vecs_wiki.json'
dict_output = [3,5,10,20,30]


#output word vectors as key value pair in json
with open(codenames_output, 'w') as f:
    json.dump(codenames_vecs, f)

for i in dict_output:
    with open('../data/processed_data/dictionary_vecs_wiki_' + str(i) + 'k.json', 'w') as f:
        json.dump(dictionary_vecs[i], f)
