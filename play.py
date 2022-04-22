from game_engine import Wordle
from game_agent import WordleAI

def real_wordle_word_bank():
    import csv

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

def real_wordle_w_ai_assist():
    word_bank = real_wordle_word_bank()
    new_game = Wordle(answer=None, word_bank=word_bank)
    ai = WordleAI(new_game)
    while True:
        use_ai = input("Get help from a.i? [y/n]: ")
        if use_ai == "y":
            options = ai.get_viable_guesses()
            print(f"Given your previous guesses, there are {len(options)} potential words")
            if len(options) < 3:
                print("The best guesses are ", end="")
                for idx, option in enumerate(options):
                    if idx == len(options)-1:
                        end = ""
                    else:
                        end = ", "
                    print(f"{option}", end=end)
                print()
            else:
                print(f"The best guesses are {options[0]}, {options[1]}, {options[2]}")

        new_game.guess()
        new_game.render_result()

def watch_ai_play():
    word_bank = real_wordle_word_bank()
    new_game = Wordle(answer=None, word_bank=word_bank, ai=True)
    ai = WordleAI(new_game)
    while True:
        guess = ai.random_viable_guess()
        new_game.evaluate_guess(guess)
        new_game.render_result()

if __name__ == "__main__":
    # real_wordle()
    # real_wordle_w_ai_assist()
    watch_ai_play()
