import numpy as np
import json

class WordBase:
    def __init__(self, codenames_file, dictionary_file):
        self.codenames_words = self.load_data(codenames_file)
        self.dictionary_words = self.load_data(dictionary_file)
        self.map_codenames_to_dictionary()
        codenames_vecs = np.array([word.get_vector() for word in self.codenames_words])
        dictionary_vecs = np.array([word.get_vector() for word in self.dictionary_words])
        self.cosine_sim_mat = self.compute_cosine_sim_mat(codenames_vecs, dictionary_vecs) # SHAPE = (NUM_DICT, NUM_CODENAMES)
        
    def load_data(self, file):
        with open(file) as f:
            content = json.load(f)
        words = np.array(list(content.keys()))
        vecs = np.array(list(content.values()))
        word_list = [Word(words[i], i, vecs[i]) for i in range(len(words))]
        return word_list
        
    def compute_cosine_sim_mat(self, codenames_vecs, dictionary_vecs):
        return np.matmul(dictionary_vecs, codenames_vecs.T)
    
    def map_codenames_to_dictionary(self):
        '''
        Make two mappings between codenames words and dictionary words
        '''
        self.cn_to_dict = dict()
        self.dict_to_cn = dict()
        for cn_word in self.codenames_words:
            match_idx = np.argwhere(self.dictionary_words==cn_word)
            if len(match_idx) == 0:
                self.dictionary_words.append(cn_word)
            match_idx = np.argwhere(self.dictionary_words==cn_word)
            dict_word = self.dictionary_words[match_idx[0][0]]
            self.cn_to_dict[cn_word.word] = dict_word
            self.dict_to_cn[dict_word.word] = cn_word
            
        return None
        
    def get_codenames_words(self):
        return self.codenames_words
    
    def get_dictionary_words(self):
        return self.dictionary_words
    
    def get_cosine_sim_mat(self):
        return self.cosine_sim_mat
    
    def get_cn_to_dict(self):
        return self.cn_to_dict
    
    def get_dict_to_cn(self):
        return self.dict_to_cn
        
        
class Word:
    def __init__(self, word, index, vector):
        self.word = word
        self.index = index
        self.vector = vector
    
    def get_word(self):
        return self.word
        
    def get_index(self):
        return self.index
        
    def get_vector(self):
        return self.vector
    
    def __eq__(self, other_word):
        if type(other_word) == str:
            return self.word == other_word
        elif type(other_word) == list:
            return [self.word==x.word for x in other_word]
        else:
            return self.word == other_word.word
    
    def __str__(self):
        return self.word
        
    def __lt__(self, other_word):
        return self.word < other_word.word
    
    
