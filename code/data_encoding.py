import os

mypath = '../../AI_dataset' #file that stores all data, should be in same directory as git repo
file = [os.path.join(mypath, f) for f in os.listdir(mypath) if not f.startswith('.')] #gets name of all 33 datafile, ignores .DS_Store file
key = range(1, 34)

data_encodings = dict(zip(key, file))
