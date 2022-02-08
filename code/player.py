import numpy as np
from wordBase import WordBase, Word
import time
import re


class Player:

    def __init__(self, player_type, teammate_type, word_base, game_words, guess_status, team, role, seed):
        self.game_words = game_words
        self.guess_status = guess_status
        self.role = role
        # Assign word belongings
        if team == 'a':
            self.team_words = game_words[:9]
            self.opponent_words = game_words[9:17]
        else:
            self.team_words = game_words[9:17]
            self.opponent_words = game_words[:9]
        self.neutral_words = game_words[17:24]
        self.assassin_word =  game_words[24]
        # Initiate Player instances
        if player_type == 'ai':
            self.player = AI(teammate_type, word_base, seed)
        else:
            self.player = Human(word_base)
    
    def give_hint(self):
        return self.player.give_hint(
            self.game_words,
            self.guess_status,
            self.team_words,
            self.opponent_words,
            self.neutral_words,
            self.assassin_word
        )
    
    def make_guess(self, hint, number):
        return self.player.make_guess(hint, number, self.game_words, self.guess_status)
    
    
class AI():
    
    def __init__(self, teammate_type, word_base, seed):

        np.random.seed(seed)
        self.teammate = teammate_type

        self.word_base = word_base
        self.conservative_base = word_base.get_conservative_base()
        self.conservative_increment = word_base.get_conservative_increment()
        self.human_threshold = word_base.get_threshold()

        self.sim_mat = word_base.get_sim_mat()
        confusing_sd = 0.025 # MAGIC NUMBER
        self.confusing_sim_mat = self.sim_mat + np.random.normal(0, confusing_sd, self.sim_mat.shape)
    
    def give_hint(self, game_words, guess_status, team_words, opponent_words, neutral_words, assassin_word):
        untouched_words = game_words[np.argwhere(guess_status<=0).T][0]
        untouched_team_words = np.intersect1d(team_words, untouched_words)
        untouched_opponent_words = np.intersect1d(opponent_words, untouched_words)
        untouched_neutral_words = np.intersect1d(neutral_words, untouched_words)

        ci = np.max([self.conservative_base + (25 - len(untouched_words)) * self.conservative_increment, 1])
        score = self.compute_score(untouched_team_words, untouched_neutral_words, untouched_opponent_words, assassin_word, ci)

        untouched_idx_in_dict = [self.word_base.get_cn_to_dict()[word.get_word()].get_index() for word in untouched_words]
        max_score_id = -1
        max_score = 0
        for i in range(self.sim_mat.shape[0]):
            if (i not in untouched_idx_in_dict) and (score[i, 1] > max_score):
                max_score_id = i
                max_score = score[i, 1]
        
        return self.word_base.get_dictionary_words()[max_score_id], int(score[max_score_id, 0])
        
    def compute_score(self, team_words, neutral_words, opponent_words, assassin_word, ci): 
        team_words_id = [word.get_index() for word in team_words]
        neutral_words_id = [word.get_index() for word in neutral_words]
        opponent_words_id = [word.get_index() for word in opponent_words]
        assassin_word_id = assassin_word.get_index()
        ret = []
        for i in range(self.sim_mat.shape[0]):
            lower_bound = np.max(np.concatenate([self.sim_mat[i, neutral_words_id] * 1.05,
                self.sim_mat[i, opponent_words_id] * 1.1,
                self.sim_mat[i, assassin_word_id] * 1.2],
                axis = None
            ))
            # Human interpretable boundary
            if self.teammate == 'human':
                lower_bound = np.max([lower_bound, self.human_threshold])
            # Get ally word scores that are higher than the bound
            valid_scores = self.sim_mat[i, np.where(self.sim_mat[i, team_words_id] > lower_bound * ci)][0]
            suggested_count = len(valid_scores)
            if suggested_count > 0:
                # Compute the numerical space between lower bound and the lowest score of the valid ally words (can be negative)
                safe_space = np.min(valid_scores) - lower_bound
            else:
                safe_space = 0
            modified_score = suggested_count + safe_space
            ret.append([suggested_count, modified_score])
        ret = np.array(ret)
        return ret
    
    def make_guess(self, hint, number, game_words, guess_status):
        untouched_words = game_words[np.argwhere(guess_status<=0).T][0]
        untouched_words_id = [word.get_index() for word in untouched_words]
        relevant_scores = self.confusing_sim_mat[hint.get_index(), untouched_words_id]
        idx_top_k = np.argpartition(relevant_scores, -number)[-number:]
        idx_top_k_sorted = idx_top_k[np.argsort(relevant_scores[idx_top_k])][::-1]
        return untouched_words[idx_top_k_sorted]

class Human():
    def __init__(self, word_base):
        self.word_base = word_base
    
    def give_hint(self, game_words, guess_status, team_words, opponent_words, neutral_words, assassin_word):
        while True:
            user_input = input("It\'s your turn to give a hint. Please type in the word and number of your hint, separated by a single space: ")
            if len(re.findall('^[A-Za-z]+ [0-9]$', user_input)) == 0:
                print("Please check the format of your input and attempt again.")
                continue
            word, count = user_input.split()
            if word not in self.word_base.get_dictionary_words():
                print("Sorry, the word \"{}\" you just inputed is not in our current word base, please try another word.".format(word))
                time.sleep(1)
            else:
                break
        word_obj = self.word_base.get_dictionary_words()[np.where([x==word for x in self.word_base.get_dictionary_words()])[0][0]]
        return word_obj, int(count)
    
    def make_guess(self, hint, number, game_words, guess_status):
        while True:
            guesses = input("Please type in your guesses in order separated by a single space. The maximum number of guesses allowed is {}: ".format(number + 1))
            guesses = guesses.split()
            valid_input = True
            for word in guesses:
                if word not in game_words or guess_status[np.argwhere(game_words == word)[0]] != 0:
                    print("Sorry, the word {} you just inputed is not on the board, please try again.")
                    valid_input = False
            if valid_input == True and len(guesses) <= number + 1:
                break
        return guesses
    