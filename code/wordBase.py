import numpy as np
import json
from nltk.corpus import wordnet as wn

class WordBase:
    def __init__(self, data_file):
        self.codenames_words, self.dictionary_words, self.sim_mat = self.load_data(data_file)
        self.map_codenames_to_dictionary()
        self.data_file_name = data_file.split('/')[-1]
    
    def load_data(self, data_file):
        data = np.load(data_file, allow_pickle=True)
        cn_words_txt = data['codenames_words']
        dt_words_txt = data['dictionary_words']
        sim_mat = data['matrix']
        cn_words = [Word(cn_words_txt[i], i) for i in range(len(cn_words_txt))]
        dt_words = [Word(dt_words_txt[i], i) for i in range(len(dt_words_txt))]
        return cn_words, dt_words, sim_mat
    
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
    
    def get_sim_mat(self):
        return self.sim_mat
    
    def get_cn_to_dict(self):
        return self.cn_to_dict
    
    def get_dict_to_cn(self):
        return self.dict_to_cn
    
    def get_data_file_name(self):
        return self.data_file_name

        
class Word:
    def __init__(self, word, index):
        self.word = word
        self.index = index
    
    def get_word(self):
        return self.word
        
    def get_index(self):
        return self.index
    
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
    
    
