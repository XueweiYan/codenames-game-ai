import os
import numpy as np

conservative_base = 0.95
conservative_increment = 0.0

print(" "*20 + "--- CODENAMES GAME WITH AI ---")
print("Please follow the instructions below to type in the settings for your game...")

ta_ms = str(input("Choose the player for TEAM A Spymaster [1. Human / 2. AI]:  "))
ta_gs = str(input("Choose the player for TEAM A Guesser [1. Human / 2. AI]:  "))
tb_ms = str(input("Choose the player for TEAM B Spymaster [1. Human / 2. AI]:  "))
tb_gs = str(input("Choose the player for TEAM B Guesser [1. Human / 2. AI]:  "))
players = " ".join([ta_ms, ta_gs, tb_ms, tb_gs])

mode = input("Please set the mode for this game. Press enter to skip [normal / pure_ai / debug]: ")
mode = mode if mode != "" else 'normal'

alg = input("Choose the algorithm for this game. If no preference, press enter to skip [1. Alg 1 / 2. Alg 2]: ")
alg = int(alg) if alg != "" else 1
data_file = input("Choose the data file for this game. If no preference, press enter to skip [TODO OPTIONS]: ")
data_file = int(data_file) if data_file != "" else 1

seed = input("Please enter the random seed for this game. If no preference, press enter to skip: ")
seed = int(seed) if seed!="" else np.random.randint(2**31 - 1)

cmd = 'python codenames.py -p {} -m {} -a {} -d {} -cb {} -ci {} -s {}'.format(players, mode, alg, data_file, conservative_base, conservative_increment, seed)
os.system(cmd)
