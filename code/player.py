import numpy as np

class Player:
    def __init__(self, player_type, game_words, guess_status, cosine_sim_mat, mapping_dict, team):
        self.game_words = game_words
        self.guess_status = guess_status
        if team == 'a':
            self.team_words_id = np.arange(9)
        else:
            self.team_words_id = np.arange(9, 17)
        if player_type == 'ai':
            self.player = AI(cosine_sim_mat, mapping_dict)
        else:
            self.player = Human()
        
    def give_hint(self):
        return self.player.give_hint(self.game_words, self.guess_status, self.team_words_id)
    
    def make_guess(self, hint, number):
        return self.player.make_guess(hint, number, self.game_words, self.guess_status)
    
    def update_game_status(self, guess_status):
        self.guess_status = guess_status
    
    
    
class AI():
    
    def __init__(self, cosine_sim_mat, mapping_dict, threshold=0.1, conservative_index = 0.5):
        self.cosine_sim_mat = cosine_sim_mat
        self.confused_cosine_sim_mat = cosine_sim_mat + np.random.normal(0, 0.03, cosine_sim_mat.shape)  # MAGIC NUMBER
        self.mapping_dict = mapping_dict
        self.threshold = threshold
        self.conservative_index = conservative_index
    
    def give_hint(self, game_words, guess_status, team_words_id):
        untouched_words = game_words[np.argwhere(guess_status<=0).T][0]
        untouched_team_words = np.intersect1d(game_words[team_words_id], untouched_words)
        untouched_enemy_words = np.intersect1d(np.delete(game_words, team_words_id), untouched_words)
        assassin_word = game_words[-1]
        score = self.compute_score(untouched_team_words, untouched_enemy_words, assassin_word)
        untouched_idx_in_dict = [self.mapping_dict[x] for x in untouched_words]
        
        max_score_id = -1
        max_score = 0
        for i in range(self.cosine_sim_mat.shape[0]):
            if (i not in untouched_idx_in_dict) and (score[i, 2] > max_score):
                max_score_id = i
                max_score = score[i, 2]
        return max_score_id, int(score[max_score_id, 1])
        
    def compute_score(self, team_words, enemy_words, assassin_word):
        ret = []
        for i in range(self.cosine_sim_mat.shape[0]):
            lower_bound = np.max(
                self.cosine_sim_mat[i, enemy_words] + [self.cosine_sim_mat[i, assassin_word] + 0.1] + [self.threshold]    # MAGIC NUMBER
            )
            suggested_count = np.sum(self.cosine_sim_mat[i, team_words] > lower_bound * self.conservative_index)
            weighted_score = np.square(lower_bound) * suggested_count
            ret.append([lower_bound, suggested_count, weighted_score])
        ret = np.array(ret)
        return ret
        
    def make_guess(self, hint, number, game_words, guess_status):
        untouched_words = game_words[np.argwhere(guess_status<=0).T][0]
        relevant_scores = self.confused_cosine_sim_mat[hint, untouched_words]
        idx_top_k = np.argpartition(relevant_scores, -number)[-number:]
        idx_top_k_sorted = idx_top_k[np.argsort(relevant_scores[idx_top_k])][::-1]
        return untouched_words[idx_top_k_sorted]
    
