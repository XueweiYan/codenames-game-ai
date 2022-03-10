# codenames-game-ai

In this project, we attempt to create several methods for an AI to simulate playing the popular board game Codenames in Python.

## Retrieve Data

Due to their size, the processed datasets used in the game are stored separately in a public google drive. Here is the link to download them.

https://drive.google.com/drive/folders/1FqEHYL_uTQDQ_MFw8T4gdD4VHaa2r0jv?usp=sharing

Please save the folder outside this repository but in the same folder. Rename the folder with the processed data as "AI_dataset".

## Environment Setup

### Local

* If you wish to run the game on a local Python environment, clone this repository into a storage folder of your choice and follow the directions for retrieving the data above.

* The Codenames code uses several python packages for data processing and display. They are:
  - nltk
  - termcolor
  - tqdm

* Use `pip install` or `conda install` to install these packages in your local Python environment, depending on which your environment uses.

### Docker

We also provide the dockerfile and docker image that contains the packages needed for running the game:
* Dockerfile: provided in this repository
* Docker image: `yongqingli/codename_ai:latest`

## Instructions

### Running the game

* Once the data has been retrieved and packages downloaded, simply run `python run.py` and choose if you wish to watch an AIvsAI game or choose the game's parameters for yourself.

* Follow the instructions to generate your own Codenames game.

## Data Collection
Our system provides 3 datasets to serve as the AI vocabulary base:
* GloVe: 
  * pretrained word embeddings from Wikipedia
  * cosine similarity
* Word2Vec
  * word embeddings trained from the English Simple Wiki using the gensim word2vec model
  * we converted all letters to lowercase, removed punctuations, and tokenized all words in the corpus
  * cosine similarity
* WordNet
  * pretrained word embeddings from the WordNet dataset
  * Wu-Palmer similiarity

## Citations

Codenames word list: [https://boardgamegeek.com/thread/1413932/word-list](https://boardgamegeek.com/thread/1413932/word-list) (User: Steven Traver)

Most common English words: [https://github.com/first20hours/google-10000-english](https://github.com/first20hours/google-10000-english)
