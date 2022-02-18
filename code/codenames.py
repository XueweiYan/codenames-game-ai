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

    def record_statistics(self, turn, assassin, accuracy):
        with open(self.output_file, 'a') as f:
            f.write(",".join([turn, assassin] + accuracy + [self.word_base.get_data_file_name(), str(self.seed)]) + "\n")
        return None
    
    def play(self):
        turn = 1
        assassin = False
        game_accuracy = [0, 0, 0, 0] #[#intended correct, #unintended correct, #wrong, #total intended]
        while True:
            # TEAM A GIVE HINT
            if isinstance(self.ta_ms.player, Human) or isinstance(self.ta_gs.player, AI):
                self.display_board(self.word_team, 'A', turn)
                time.sleep(4 * (self.mode=='interactive'))
            word, count = self.ta_ms.give_hint()

            # AI-Human testing: ta_ms = AI, ta_gs = Human
            intended_words = self.ta_ms.make_guess(word, count)
            game_accuracy[3] += count

            # TEAM A GUESS
            self.display_board(self.guess_status, 'A', turn)
            print("TEAM A Spymaster: My hint is {}: {}".format(word, count))
            guess = self.ta_gs.make_guess(word, count)
            for word in guess:
                time.sleep(2 * (self.mode=='interactive'))
                print("TEAM A Guesser: I guess \"{}\" is our word".format(word))
                idx_in_game_words = np.argwhere(self.game_words == word)
                time.sleep(1.5 * (self.mode=='interactive'))
                if idx_in_game_words < 9:
                    # AI-Human testing
                    if word in intended_words: #correct intended
                        game_accuracy[0] += 1
                    else: #correct unintended
                        game_accuracy[1] += 1
                    print("TEAM A Spymaster: That is correct!")
                    self.guess_status[idx_in_game_words] = 1
                elif idx_in_game_words < 17:
                    print("TEAM A Spymaster: That is incorrect... It is the opponents' word...")
                    self.guess_status[idx_in_game_words] = 2
                    game_accuracy[2] += 1
                    break
                elif idx_in_game_words < 24:
                    print("TEAM A Spymaster: That is incorrect... It is a neutral word...")
                    self.guess_status[idx_in_game_words] = 3
                    game_accuracy[2] += 1
                    break
                else:
                    print("TEAM A Spymaster: That is incorrect... It is the assassin word...")
                    self.guess_status[idx_in_game_words] = 4
                    game_accuracy[2] += 1
                    assassin = True
                    break
            
            # TEAM A FINISH
            if self.check_game_end('A', turn):
                break
            print("END OF TURN")
            time.sleep(2 * (self.mode=='interactive'))

            # TEAM B GIVE HINT
            if isinstance(self.tb_ms.player, Human) or isinstance(self.tb_gs.player, AI):
                self.display_board(self.word_team, 'B', turn)
                time.sleep(4 * (self.mode=='interactive'))
            word, count = self.tb_ms.give_hint()
            
            # AI-Human testing: tb_ms = AI, tb_gs = Human
            intended_words = self.tb_ms.make_guess(word, count)
            game_accuracy[3] += count

            # TEAM B GUESS
            self.display_board(self.guess_status, 'B', turn)
            print("TEAM B Spymaster: My hint is {}: {}".format(word, count))
            guess = self.tb_gs.make_guess(word, count)
            for word in guess:
                time.sleep(2 * (self.mode=='interactive'))
                print("TEAM B Guesser: I guess \"{}\" is our word".format(word))
                idx_in_game_words = np.argwhere(self.game_words == word)
                time.sleep(1.5 * (self.mode=='interactive'))
                if idx_in_game_words < 9:
                    print("TEAM B Spymaster: That is incorrect... It is the opponents' word...")
                    self.guess_status[idx_in_game_words] = 1
                    game_accuracy[2] += 1
                    break
                elif idx_in_game_words < 17:
                    print("TEAM B Spymaster: That is correct!")
                    self.guess_status[idx_in_game_words] = 2
                    # AI-Human testing
                    if word in intended_words: #correct intended
                        game_accuracy[0] += 1
                    else: #correct unintended
                        game_accuracy[1] += 1
                elif idx_in_game_words < 24:
                    print("TEAM B Spymaster: That is incorrect... It is a neutral word...")
                    self.guess_status[idx_in_game_words] = 3
                    game_accuracy[2] += 1
                    break
                else:
                    print("TEAM B Spymaster: That is incorrect... It is the assassin word...")
                    self.guess_status[idx_in_game_words] = 4
                    game_accuracy[2] += 1
                    assassin = True
                    break
            # TEAM B FINISH
            if self.check_game_end('B', turn):
                break
            print("END OF TURN")
            time.sleep(2 * (self.mode=='interactive'))

            turn += 1
        
        # Wrap up and Recording
        print("For reproducibility, the random seed used in this game is {}.".format(self.seed))
        if self.output_file != None:
            self.record_statistics(str(turn), str(assassin), [str(i) for i in game_accuracy])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--players', type=int, nargs='+', default=[2, 2, 2, 2], help='list of player types [1. Human / 2. AI]')
    parser.add_argument('-m', '--mode', type=str, default='interactive', help='mode of the game (interactive / testing)')
    parser.add_argument('-d', '--data_file', type=int, default=1, help='dataset used by AI in the game (1. cosine_wiki_30k / 2. wup_wiki_30k)')
    parser.add_argument('-s', '--seed', type=int, default=np.random.randint(2**31 - 1), help='random seed used in this game (0 - 2^31-1)')
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
