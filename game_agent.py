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

        gray_letters = set()
        yellow_letters = set()
        green_letters_w_idx = set()
        yellow_letters_w_idx = []
        
        for guess in past_guesses:
           for (color, letter, idx) in guess:
               if color == "grey":
                   gray_letters.add(letter)
               elif color == "green":
                   green_letters_w_idx.add((letter, idx))
               elif color == "yellow":
                   yellow_letters_w_idx.append((letter, idx))
                   yellow_letters.add(letter)

        possible_words = self.filter_by_green(green_letters_w_idx, possible_words)

        possible_words = self.filter_by_gray(gray_letters, yellow_letters, green_letters_w_idx, possible_words)
        possible_words = self.filter_by_yellow(yellow_letters_w_idx, possible_words)
        return possible_words

    def filter_by_green(self, green_letters_w_idx, possible_words):
        green_words = []
        for word in possible_words:
            cond = all(word[idx] == letter for (letter, idx) in green_letters_w_idx)
            if cond:
                green_words.append(word)

        return green_words

    def filter_by_gray(self, gray_letters, yellow_letters, green_letters_w_idx, possible_words):
        gray_words = []
        for word in possible_words:
            cond = True
            for idx, letter in enumerate(word):
                if letter in gray_letters:
                    # even if the letter is gray
                    # if you are correctly using the
                    # the letter in a green word
                    # the letter is ok
                    if (idx, letter) in green_letters_w_idx:
                        continue

                    # even if the letter is gray
                    # if the letter is also in yellow
                    # allow it.
                    if letter in yellow_letters:
                        continue

                    cond = False

            if cond:
                gray_words.append(word)

        return gray_words

    def filter_by_yellow(self, yellow_letters_w_idx, possible_words):
        yellow_words = []
        for word in possible_words:
            cond = True
            for (letter, idx) in yellow_letters_w_idx:
                if letter in word and word[idx] != letter: 
                    pass
                else:
                    cond = False

            if cond:
                yellow_words.append(word)

        return yellow_words
