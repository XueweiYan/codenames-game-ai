import os
import numpy as np
from tqdm import tqdm


outfile = "../ai_human_stats.csv"
num_games = 33
data = ["1", "2", "3"] #key for target data


with open(outfile, 'a') as f:
    f.write(",".join(['turn', 'assassin', 'intended correct', 'unintended correct', 'wrong', 'total intended', 'data', 'seed']) + "\n")


seeds = [str(i) for i in np.random.randint(2**31 - 1, size = (num_games))]
#loop through each datasets and record performance
d_num = 1
for d in data:
	print('----- data={}/{}'.format(d_num, len(data)))
	d_num += 1
	for s in tqdm(seeds):
		cmd = 'python codenames.py -p 2 1 2 1 -m testing -d {} -s {} -o {}'.format(d, s, outfile)
		os.system(cmd)
		game += 1

