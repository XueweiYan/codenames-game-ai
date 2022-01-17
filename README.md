# codenames-game-ai


### Data Sources:

Codenames word list: https://boardgamegeek.com/thread/1413932/word-list (User: Steven Traver)

Most common English words: https://github.com/first20hours/google-10000-english

### Updates:

##### 2022.1.9 First Demo

- Preprocessed word list data and their vector embeddings.

- implmented a tiny demo that can have the AI generate hints and guesses through notebooks. The main goal is to test the use of different packages and find the optimal way to develop OOP structure for later versions.

##### 2022.1.15 Version 0.1

- Only support full AI automated game play, human actions to be implemented.

- Implemented a confusing adjustment to guesser AI's word-to-vec knowledge space so that AI may make wrong guesses by chance. Can adjust the level of confusion by the standard deviation of the normal distribution.

- Implemented a conservative index (ranged 0~1, with 1 being the most conservative spymaster, now set to 0.7). This index represents the potential risk the spymaster is willing to take in exchange for guessing more words in a single round.

##### 2022.1.16 Version 1.0

- Redo the structure of the code base, introduced Word and Word Base object for better translation between human and AI.

- Full functions of the game implemented, now the game can be played through `cd code`, then `python codenames.py`. Now, we only have one set of strategy and one set of vector embeddings, we will focus on getting more options and test for the optimal for later updates.
