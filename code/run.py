import os
import numpy as np

print(" "*20 + "--- CODENAMES GAME WITH AI ---")
print("Please follow the instructions below to type in the settings for your game...")

ta_ms = str(input("Choose the player for TEAM A Spymaster [1. Human / 2. AI]:  "))
ta_gs = str(input("Choose the player for TEAM A Guesser [1. Human / 2. AI]:  "))
tb_ms = str(input("Choose the player for TEAM B Spymaster [1. Human / 2. AI]:  "))
tb_gs = str(input("Choose the player for TEAM B Guesser [1. Human / 2. AI]:  "))
players = " ".join([ta_ms, ta_gs, tb_ms, tb_gs])

mode = input("Please set the mode for this game. Press enter to skip [interactive / testing]: ")
mode = mode if mode != "" else 'interactive'

data_file = input("Choose the data file for this game. If no preference, press enter to skip [1. GloVe / 2. Word2Vec 3./ WordNet]: ")
data_file = int(data_file) if data_file != "" else 1

seed = input("Please enter the random seed for this game. If no preference, press enter to skip: ")
seed = int(seed) if seed!="" else np.random.randint(2**31 - 1)

cmd = 'python codenames.py -p {} -m {} -d {} -s {}'.format(players, mode, data_file, seed)
os.system(cmd)
