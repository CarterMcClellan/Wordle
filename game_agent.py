from game_engine import Wordle
from random import choice


class WordleAI:
    def __init__(self, game: Wordle):
        self.game = game
        self.word_bank = game.get_word_bank()

    def random_viable_guess(self,):
        viable_guesses = self.get_viable_guesses()
        return choice(viable_guesses)

    def get_viable_guesses(self):
        past_guesses = self.game.get_past_guesses()
        possible_words = self.word_bank

        ###########################################
        # Write your implementation here
        ###########################################
        return
