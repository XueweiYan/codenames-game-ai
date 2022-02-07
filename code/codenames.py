import numpy as np
import json
from termcolor import colored, cprint
from player import Player, AI, Human
from wordBase import WordBase, Word
from data_encoding import data_encodings
import argparse
import time
import os


class Codenames:
    def __init__(self, players, mode, data_file, seed, output_file):
        self.mode = mode
        self.seed = seed
        self.output_file = output_file
        np.random.seed(self.seed)
        self.assassin = False #for testing purpose only
        self.word_base = WordBase(data_encodings[data_file])
        self.initiate_game()
        self.initiate_players(players)

    def initiate_game(self):
        # Randomly choose 25 words and assign to teams (9 -> red,8 -> blue,7 -> neutral,1 -> assassin)
        self.game_words = np.random.choice(self.word_base.get_codenames_words(), 25, replace=False)
        self.guess_status = np.zeros(25)
        self.word_team = [1] * 9 + [2] * 8 + [3] * 7 + [4]
        # Resuffle for random display
        self.display_order = np.random.choice(range(25), 25, replace=False)
        return None
    
    def initiate_players(self, players):
        self.ta_ms = Player(players[0], players[1], self.word_base, self.game_words, self.guess_status, 'a', 'spymaster', self.seed)
        self.ta_gs = Player(players[1], players[0], self.word_base, self.game_words, self.guess_status, 'a', 'guesser', self.seed)
        self.tb_ms = Player(players[2], players[3], self.word_base, self.game_words, self.guess_status, 'b', 'spymaster', self.seed)
        self.tb_gs = Player(players[3], players[2], self.word_base, self.game_words, self.guess_status, 'b', 'guesser', self.seed)
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
        if self.mode == 'pure_ai':
            self.play_AI()
            return None
        
        turn = 1
        while True:

            # if isinstance(self.ta_ms.player, Human): #only display card identities when the spymaster is a human       
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
            

            # if isinstance(self.tb_ms.player, Human): #only display card identities when the spymaster is a human       
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
        
        print("For reproducibility, the random seed used in this game is {}.".format(self.seed))


    def play_AI(self):
        turn = 1
        while True:
            
            word, count = self.ta_ms.give_hint()
            
            guess = self.ta_gs.make_guess(word, count)
            for word in guess:
                idx_in_game_words = np.argwhere(self.game_words == word)
                if idx_in_game_words < 9:
                    self.guess_status[idx_in_game_words] = 1
                elif idx_in_game_words < 17:
                    self.guess_status[idx_in_game_words] = 2
                    break
                elif idx_in_game_words < 24:
                    self.guess_status[idx_in_game_words] = 3
                    break
                else:
                    self.guess_status[idx_in_game_words] = 4
                    break
            if 0 not in self.guess_status[:9] or 0 not in self.guess_status[9:17]:
                break 
            elif self.guess_status[-1] != 0:
                self.assassin = True
                break      


            word, count = self.tb_ms.give_hint()
            
            guess = self.tb_gs.make_guess(word, count)
            for word in guess:
                idx_in_game_words = np.argwhere(self.game_words == word)
                if idx_in_game_words < 9:
                    self.guess_status[idx_in_game_words] = 1
                    break
                elif idx_in_game_words < 17:
                    self.guess_status[idx_in_game_words] = 2
                elif idx_in_game_words < 24:
                    self.guess_status[idx_in_game_words] = 3
                    break
                else:
                    self.guess_status[idx_in_game_words] = 4
                    break
            if 0 not in self.guess_status[:9] or 0 not in self.guess_status[9:17]:
                break 
            elif self.guess_status[-1] != 0:
                self.assassin = True
                break
            
            turn += 1

        #record results
        with open(self.output_file, 'a') as f:
            f.write(",".join([str(turn), str(self.assassin), self.word_base.get_data_file_name(), str(self.seed)]) + "\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--players', type=int, nargs='+', default=[2, 2, 2, 2], help='list of player types [1. Human / 2. AI]')
    parser.add_argument('-m', '--mode', type=str, default='normal', help='mode of the game (normal / pure_ai / debug)')
    parser.add_argument('-d', '--data_file', type=int, default=1, help='dataset used by AI in the game (1 - 33)')
    parser.add_argument('-s', '--seed', type=int, default=np.random.randint(2**31 - 1), help='random seed used in this game (0 - 2^32-1)')
    parser.add_argument('-o', '--output_file', type=str, default=None, help='the file to record statistics')
    opt = parser.parse_args()

    input_encoding = {1: 'human', 2: 'ai'}
    game = Codenames(
        [input_encoding[p] for p in opt.players],
        opt.mode,
        opt.data_file,
        opt.seed,
        opt.output_file
    )

    game.play()
