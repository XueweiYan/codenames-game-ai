import numpy as np
import json
from termcolor import colored
from player import Player
import time

class Codenames:
    def __init__(self,
                team_a_spymaster,
                team_a_guesser,
                team_b_spymaster,
                team_b_guesser,
                codenames_file='../data/processed_data/codenames_vecs.json',
                dictionary_file='../data/processed_data/dictionary_vecs.json',
                threshold=0.1
    ):
    
        self.codenames_words, self.codenames_vecs = self.load_data(codenames_file)
        self.dictionary_words, self.dictionary_vecs = self.load_data(dictionary_file)
        self.threshold = threshold
        self.initiate_game()
        self.initiate_players(team_a_spymaster, team_a_guesser, team_b_spymaster, team_b_guesser)

    def load_data(self, file):
        with open(file) as f:
            content = json.load(f)
        words = np.array(list(content.keys()))
        vecs = np.array(list(content.values()))
        return words, vecs

    def initiate_game(self):
        # Randomly choose 25 words and assign to teams (9 -> red,8 -> blue,7 -> neutral,1 -> assassin)
        self.game_words = np.random.choice(range(len(self.codenames_words)), 25, replace=False)
        self.guess_status = np.zeros(25)
        # Resuffle for random display
        self.display_order = np.random.choice(range(25), 25, replace=False)
        # Compute cosine similarity matrix, shape = (NUM_DICT, NUM_CODENAMES)
        self.cosine_sim_mat = np.matmul(self.dictionary_vecs, self.codenames_vecs.T)
        # Make a mapping of codenames words id to dictionary words id
        self.mapping_dict = dict()
        for idx in self.game_words:
            match_idx = np.where(self.dictionary_words==self.codenames_words[idx])[0]
            if len(match_idx) > 0:
                self.mapping_dict[idx] = match_idx[0]
            else:
                self.mapping_dict[idx] = None
        return None
    
    def initiate_players(self, team_a_spymaster, team_a_guesser, team_b_spymaster, team_b_guesser):
        self.ta_ms = Player(team_a_spymaster, self.game_words, self.guess_status, self.cosine_sim_mat, self.mapping_dict, team='a')
        self.ta_gs = Player(team_a_guesser, self.game_words, self.guess_status, self.cosine_sim_mat, self.mapping_dict, team='a')
        self.tb_ms = Player(team_b_spymaster, self.game_words, self.guess_status, self.cosine_sim_mat, self.mapping_dict, team='b')
        self.tb_gs = Player(team_b_guesser, self.game_words, self.guess_status, self.cosine_sim_mat, self.mapping_dict, team='b')
        self.all_players = [self.ta_ms, self.ta_gs, self.tb_ms, self.tb_gs]
        return None
        
    def display_board(self):
        color_ref = {0: 'yellow', 1: 'red', 2: 'blue', 3: 'white', 4: 'black'}
        for i in range(5):
            for j in range(5):
                word = self.codenames_words[self.game_words[self.display_order[i*5+j]]]
                color = color_ref[self.guess_status[self.display_order[i*5+j]]]
                print(colored(word, color).center(40), end='')
            print("\n")
        return None
        
    def play(self):
        while True:
            print("*" * 145)
            print("*" + " " * 65 + "TEAM A's turn" + " " * 65 + "*")
            print("*" * 145)
            self.display_board()
            time.sleep(5)
            word_id, word_count = self.ta_ms.give_hint()
            print("TEAM A Spymaster: My hint is {}: {}".format(self.dictionary_words[word_id], word_count))
            guess = self.ta_gs.make_guess(word_id, word_count)
            for idx in guess:
                time.sleep(3)
                print("TEAM A Guesser: I guess \"{}\" is our word".format(self.codenames_words[idx]))
                idx_in_game_words = np.argwhere(self.game_words == idx)
                time.sleep(1.5)
                if idx_in_game_words < 9:
                    print("TEAM A Spymaster: That is correct!")
                    self.guess_status[idx_in_game_words] = 1
                elif idx_in_game_words < 17:
                    print("TEAM A Spymaster: That is incorrect... It is the opponents' word...")
                    self.guess_status[idx_in_game_words] = 2
                    break
                elif idx_in_game_words < 24:
                    print("TEAM A Spymaster: That is incorrect... It is a neutral word...")
                    self.guess_status[idx_in_game_words] = 3
                    break
                else:
                    print("TEAM A Spymaster: That is incorrect... It is the assassin word...")
                    self.guess_status[idx_in_game_words] = 4
                    break
            if 0 not in self.guess_status[0:9]:
                print("GAME OVER! TEAM A wins this one by finding out all their words!")
                break
            if self.guess_status[-1] != 0:
                print("GAME OVER! TEAM B wins this one as TEAM A revealed the assassin word!")
                break
            print("END OF TURN")
            time.sleep(2)
            print("*" * 145)
            print("*" + " " * 65 + "TEAM B's turn" + " " * 65 + "*")
            print("*" * 145)
            self.display_board()
            time.sleep(5)
            word_id, word_count = self.tb_ms.give_hint()
            print("TEAM B Spymaster: My hint is {}: {}".format(self.dictionary_words[word_id], word_count))
            guess = self.tb_gs.make_guess(word_id, word_count)
            for idx in guess:
                time.sleep(3)
                print("TEAM B Guesser: I guess \"{}\" is our word".format(self.codenames_words[idx]))
                idx_in_game_words = np.argwhere(self.game_words == idx)
                time.sleep(1.5)
                if idx_in_game_words < 9:
                    print("TEAM B Spymaster: That is incorrect... It is the opponents' word...")
                    self.guess_status[idx_in_game_words] = 1
                    break
                elif idx_in_game_words < 17:
                    print("TEAM B Spymaster: That is correct!")
                    self.guess_status[idx_in_game_words] = 2
                elif idx_in_game_words < 24:
                    print("TEAM B Spymaster: That is incorrect... It is a neutral word...")
                    self.guess_status[idx_in_game_words] = 3
                    break
                else:
                    print("TEAM B Spymaster: That is incorrect... It is the assassin word...")
                    self.guess_status[idx_in_game_words] = 4
                    break
            if 0 not in self.guess_status[9:17]:
                print("GAME OVER! TEAM B wins this one by finding out all their words!")
                break
            if self.guess_status[-1] != 0:
                print("GAME OVER! TEAM A wins this one as TEAM A revealed the assassin word!")
                break
            print("END OF TURN")
            time.sleep(2)

def __main__():
    team_a_spymaster = input("Choose the player for TEAM A Spymaster [1. Human / 2. AI]:  ")
    team_a_guesser = input("Choose the player for TEAM A Guesser [1. Human / 2. AI]:  ")
    team_b_spymaster = input("Choose the player for TEAM B Spymaster [1. Human / 2. AI]:  ")
    team_b_guesser = input("Choose the player for TEAM B Guesser [1. Human / 2. AI]:  ")
    input_encoding = {'1': 'human', '2': 'ai'}
    game = Codenames(
        input_encoding[team_a_spymaster],
        input_encoding[team_a_guesser],
        input_encoding[team_b_spymaster],
        input_encoding[team_b_guesser]
    )
    game.play()

if __name__ == '__main__':
    __main__()

