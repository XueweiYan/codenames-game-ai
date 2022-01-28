import numpy as np
import json
from termcolor import colored, cprint
from player import Player, AI, Human
from wordBase import WordBase, Word
from data_encoding import data_encodings
import time
import os


class Codenames:
    def __init__(self,
                team_a_ms, team_a_gs, team_b_ms, team_b_gs, alg=None,
                data_file=None,
                seed=None
    ):
        if seed != None:
            self.seed = seed
        else:
            self.seed = np.random.randint(2**32 - 1)
        np.random.seed(self.seed)

        if alg != None:
            self.alg = alg
        else:
            self.alg = 1 ####replace with the best algorithm later
        
        if data_file != None:
            self.data_file = data_encodings[data_file]
        else:
            self.data_file = '../../AI_dataset/cosine_sim_mat.npz' ####replace with best data set later

        self.word_base = WordBase(self.data_file)
        self.initiate_game()
        self.initiate_players(team_a_ms, team_a_gs, team_b_ms, team_b_gs)

    def initiate_game(self):
        # Randomly choose 25 words and assign to teams (9 -> red,8 -> blue,7 -> neutral,1 -> assassin)
        self.game_words = np.random.choice(self.word_base.get_codenames_words(), 25, replace=False)
        self.guess_status = np.zeros(25)
        self.word_team = [1] * 9 + [2] * 8 + [3] * 7 + [4]
        # Resuffle for random display
        self.display_order = np.random.choice(range(25), 25, replace=False)
        return None
    
    def initiate_players(self, team_a_ms, team_a_gs, team_b_ms, team_b_gs):
        self.ta_ms = Player(team_a_ms, self.word_base, self.game_words, self.guess_status, team='a', role='spymaster', alg = self.alg, seed=self.seed)
        self.ta_gs = Player(team_a_gs, self.word_base, self.game_words, self.guess_status, team='a', role='guesser', alg = self.alg, seed=self.seed)
        self.tb_ms = Player(team_b_ms, self.word_base, self.game_words, self.guess_status, team='b', role='spymaster', alg = self.alg, seed=self.seed)
        self.tb_gs = Player(team_b_gs, self.word_base, self.game_words, self.guess_status, team='b', role='guesser', alg = self.alg, seed=self.seed)
        return None
        
    def display_board(self, status_ref, team, turn):
        color = 'red' if team == 'A' else 'cyan'
        os.system('cls' if os.name in ('nt', 'dos') else 'clear')
        cprint("*" * 85, color)
        cprint("*" + " " * 35 + "TEAM {} TURN {}".format(team, turn) + " " * 35 + "*", color)
        cprint("*" * 85, color)
        color_ref = {0: 'yellow', 1: 'red', 2: 'cyan', 3: 'yellow', 4: 'magenta'}
        for i in range(5):
            for j in range(5):
                word = self.game_words[self.display_order[i*5+j]].word
                color = color_ref[status_ref[self.display_order[i*5+j]]]
                if self.guess_status[self.display_order[i*5+j]] != 0:
                    cprint(word.center(17), color, 'on_{}'.format(color), end='')
                else:
                    cprint(word.center(17), color, end='')
            print("\n")
        return None
    
    def check_game_end(self, team, turn):
        other_team = {'A': 'B', 'B': 'A'}
        if 0 not in self.guess_status[:9]:
            self.display_board(self.guess_status, team, turn)
            print("GAME OVER IN {} TURNS! TEAM A wins this one by finding out all their words!".format(turn))
            return True
        if 0 not in self.guess_status[9:17]:
            self.display_board(self.guess_status, team, turn)
            print("GAME OVER IN {} TURNS! TEAM B wins this one by finding out all their words!".format(turn))
            return True
        if self.guess_status[-1] != 0:
            self.display_board(self.guess_status, team, turn)
            print("GAME OVER IN {} TURNS! TEAM {} wins this one as TEAM {} revealed the assassin word!".format(turn, other_team[team], team))
            return True        
        return False

    def play(self):
        turn = 1
        while True:

            if isinstance(self.ta_ms.player, Human): #only display card identities when the spymaster is a human       
                self.display_board(self.word_team, 'A', turn)
            
            word, count = self.ta_ms.give_hint()
            time.sleep(5)
            
            self.display_board(self.guess_status, 'A', turn)
            print("TEAM A Spymaster: My hint is {}: {}".format(word, count))
            guess = self.ta_gs.make_guess(word, count)
            for word in guess:
                time.sleep(3)
                print("TEAM A Guesser: I guess \"{}\" is our word".format(word))
                idx_in_game_words = np.argwhere(self.game_words == word)
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
            if self.check_game_end('A', turn):
                break
            print("END OF TURN")
            time.sleep(2)
            
            if isinstance(self.tb_ms.player, Human): #only display card identities when the spymaster is a human       
                self.display_board(self.word_team, 'B', turn)
            
            word, count = self.tb_ms.give_hint()
            time.sleep(5)
            
            self.display_board(self.guess_status, 'B', turn)
            print("TEAM B Spymaster: My hint is {}: {}".format(word, count))
            guess = self.tb_gs.make_guess(word, count)
            for word in guess:
                time.sleep(3)
                print("TEAM B Guesser: I guess \"{}\" is our word".format(word))
                idx_in_game_words = np.argwhere(self.game_words == word)
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
            if self.check_game_end('B', turn):
                break
            print("END OF TURN")
            time.sleep(2)
            
            turn += 1
        
        #for AI-AI testing
        with open('../AI_AI_performance.csv', 'a') as f:
            f.write(str(turn) + ',' + str(self.alg) + self.data_file.split('/')[-1] + ','  + ',' + str(self.seed) + '\n')


        print("For reproducibility, the random seed used in this game is {}.".format(self.seed))

def __main__():
    ta_ms = input("Choose the player for TEAM A Spymaster [1. Human / 2. AI]:  ")
    ta_gs = input("Choose the player for TEAM A Guesser [1. Human / 2. AI]:  ")
    tb_ms = input("Choose the player for TEAM B Spymaster [1. Human / 2. AI]:  ")
    tb_gs = input("Choose the player for TEAM B Guesser [1. Human / 2. AI]:  ")
    input_encoding = {'1': 'human', '2': 'ai'}
    alg = input("Choose the algorithm for this game [1. Alg 1 / 2. Alg 2]. If no preference, press enter to skip: ")
    alg = int(alg) if alg != "" else None
    data_file = input("Choose the data file for this game (a number between 1 and 33). If no preference, press enter to skip: ")
    data_file = int(data_file) if data_file != "" else None
    seed = input("Please enter the random seed for this game. If no preference, press enter to skip: ")
    seed = int(seed) if seed!="" else None
    game = Codenames(input_encoding[ta_ms], input_encoding[ta_gs], input_encoding[tb_ms], input_encoding[tb_gs], alg, data_file, seed=seed)
    game.play()

if __name__ == '__main__':
    __main__()

