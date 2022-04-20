import csv
from game_engine import Wordle

def real_wordle_word_bank():
    word_bank = []
    with open("./wordle_wordlist.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            word_bank.append(row[0])
    return word_bank

def simple_game():
    new_game = Wordle(answer="ART", word_bank=["ART", "CAT", "HAT", "RAT", "FOO", "BAR"])
    while True:
        new_game.guess()
        new_game.render_result()

def real_wordle():
    word_bank = real_wordle_word_bank()
    new_game = Wordle(answer=None, word_bank=word_bank)
    while True:
        new_game.guess()
        new_game.render_result()

if __name__ == "__main__":
    real_wordle()
