import numpy as np
import json
from termcolor import colored, cprint
from player import Player
from wordBase import WordBase, Word
import time
import os

class Codenames:
    def __init__(self,
                team_a_ms, team_a_gs, team_b_ms, team_b_gs,
                codenames_file='../data/processed_data/codenames_vecs.json',
                dictionary_file='../data/processed_data/dictionary_vecs.json',
                threshold=0.1
    ):
    
        self.word_base = WordBase(codenames_file, dictionary_file)
        self.threshold = threshold
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
        self.ta_ms = Player(team_a_ms, self.word_base, self.game_words, self.guess_status, team='a', role='spymaster')
        self.ta_gs = Player(team_a_gs, self.word_base, self.game_words, self.guess_status, team='a', role='guesser')
        self.tb_ms = Player(team_b_ms, self.word_base, self.game_words, self.guess_status, team='b', role='spymaster')
        self.tb_gs = Player(team_b_gs, self.word_base, self.game_words, self.guess_status, team='b', role='guesser')
        return None
        
    def display_board(self, status_ref, team, turn):
        color = 'red' if team == 'A' else 'cyan'
        os.system('cls' if os.name in ('nt', 'dos') else 'clear')
        cprint("*" * 85, color)
        cprint("*" + " " * 35 + "TEAM {} TURN {}".format(team, turn) + " " * 35 + "*", color)
        cprint("*" * 85, color)
        color_ref = {0: 'yellow', 1: 'red', 2: 'cyan', 3: 'white', 4: 'magenta'}
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
        
    def play(self):
        turn = 1
        while True:
                    
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
            if 0 not in self.guess_status[0:9]:
                self.display_board(self.guess_status, 'A', turn)
                print("GAME OVER IN {} TURNS! TEAM A wins this one by finding out all their words!".format(turn))
                break
            if self.guess_status[-1] != 0:
                self.display_board(self.guess_status, 'A', turn)
                print("GAME OVER IN {} TURNS! TEAM B wins this one as TEAM A revealed the assassin word!".format(turn))
                break
            print("END OF TURN")
            time.sleep(2)
            
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
            if 0 not in self.guess_status[9:17]:
                self.display_board(self.guess_status, 'B', turn)
                print("GAME OVER IN {} TURNS! TEAM B wins this one by finding out all their words!".format(turn))
                break
            if self.guess_status[-1] != 0:
                self.display_board(self.guess_status, 'B', turn)
                print("GAME OVER IN {} TURNS! TEAM A wins this one as TEAM A revealed the assassin word!".format(turn))
                break
            print("END OF TURN")
            time.sleep(2)
            
            turn += 1

def __main__():
    ta_ms = input("Choose the player for TEAM A Spymaster [1. Human / 2. AI]:  ")
    ta_gs = input("Choose the player for TEAM A Guesser [1. Human / 2. AI]:  ")
    tb_ms = input("Choose the player for TEAM B Spymaster [1. Human / 2. AI]:  ")
    tb_gs = input("Choose the player for TEAM B Guesser [1. Human / 2. AI]:  ")
    input_encoding = {'1': 'human', '2': 'ai'}
    game = Codenames(input_encoding[ta_ms], input_encoding[tb_gs], input_encoding[ta_ms], input_encoding[tb_gs])
    game.play()

if __name__ == '__main__':
    __main__()

