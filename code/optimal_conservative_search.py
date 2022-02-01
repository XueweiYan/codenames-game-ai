import os
import numpy as np
from tqdm import tqdm

##########################
#  Change Settings Here  #
##########################
outfile = '../statistics/optimal_conservative.csv'
num_games = 100

# ------------- DO NOT TOUCH CODE BELOW --------------
if not os.path.isdir('../statistics/'):
	os.mkdir('../statistics/')
with open(outfile, 'w') as f:
    f.write(",".join(['turn', 'assassin', 'algorithm', 'data', 'seed', 'cb', 'ci']) + "\n")

algorithms = ['1', '2'] #all algorithms
data = [str(i) for i in range(1, 2)] # Iremoved all dblp datasets for this test
seeds = [str(i) for i in np.random.randint(2**31 - 1, size = (num_games))]
#loop through all combinations between algorithm, dataset, and seed
for cb in np.arange(0.8, 1.0, 0.02):
	for ci in np.arange(0.0, 0.01, 0.001):
		print('----- cb={}, ci={}'.format(cb, ci))
		for s in tqdm(seeds):
			cmd = 'python codenames.py -p 2 2 2 2 -m pure_ai -a {} -d {} -cb {} -ci {} -s {} -o {}'.format(1, 1, cb, ci, s, outfile)
			os.system(cmd)
