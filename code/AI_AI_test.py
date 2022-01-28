import subprocess
import numpy as np

algorithms = ['1', '2'] #all algorithms
data = [str(i) for i in range(1, 33)] #all 33 dataset
seeds = [str(i) for i in np.random.randint(2**32 - 1, size = (1000))] #1000 game per combination

#loop through all combinations between algorithm, dataset, and seed
for alg in algorithms:
	for d in data:
		for s in seeds:
			subprocess.call("printf '2\n2\n2\n2\n" + alg + "\n" + d + "\n" + s + "'" + "| python3 codenames.py", shell = True)


