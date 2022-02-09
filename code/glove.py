# https://github.com/stanfordnlp/GloVe

import numpy as np 
import json


# # Filepaths
# codenames_raw = '../data/raw_data/codenames_word_list.txt'
# dictionary_raw = '../data/raw_data/enwiki-20190320-words-frequency.txt'

# # Process codenames word list
# with open(codenames_raw) as f:
#     raw_text = f.readlines()

# codenames_word = set([x.strip().lower() for x in raw_text])

# # Process dictionary word list
# with open(dictionary_raw) as f:
#     raw_text = [next(f) for x in range(30000)]

# dict_words = set([x.strip().split()[0].lower() for x in raw_text])


def load_glove(file):
	glove_model = {}
	with open(file) as f:
		for l in f:
			l = l.split()
			word = l[0]
			vector = np.array(l[1:], dtype = np.float64)
			glove_model[word] = vector
	return glove_model


glove = load_glove("glove.txt")

dict_words = np.load("cosine_wiki_30k.npz", allow_pickle = True)['dictonary_words']

dictionary_vecs = {}
for i in dict_words:
	if i in glove:
		dictionary_vecs[i] = glove[i]

with open("dictionary_vecs_glove_30k.json") as f:
	json.dump(dictionary_vecs, f)




