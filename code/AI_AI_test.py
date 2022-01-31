import os
import numpy as np
from tqdm import tqdm

##########################
#  Change Settings Here  #
##########################
outfile = '../statistics/AI_AI_performance.csv'
num_games = 300

# ------------- DO NOT TOUCH CODE BELOW --------------
if not os.path.isdir('../statistics/'):
	os.mkdir('../statistics/')
with open(outfile, 'w') as f:
    f.write(", ".join(['turn', 'assassin', 'algorithm', 'data', 'seed']) + "\n")

algorithms = ['1', '2'] #all algorithms
data = [str(i) for i in range(1, 19)] # Iremoved all dblp datasets for this test
seeds = [str(i) for i in np.random.randint(2**31 - 1, size = (num_games))]
#loop through all combinations between algorithm, dataset, and seed
for alg in algorithms:
	for d in data:
		print('----- algorithm={}/2, data={}/18'.format(alg, d))
		for s in tqdm(seeds):
			cmd = 'python codenames.py -p 2 2 2 2 -m pure_ai -a {} -d {} -s {} -o {}'.format(alg, d, s, outfile)
			os.system(cmd)
