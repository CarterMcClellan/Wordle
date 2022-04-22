import os, sys, random, time
from typing import List, Union

from rich.console import Console

class Wordle:

    def __init__(self, answer: str, word_bank: List[str], ai=False):
        # TODO write some more input handlers
        if word_bank is None:
            raise Exception("You must provide a valid Word Bank")
        
        self.word_bank = word_bank
        if answer is None:
            self.answer = random.choice(word_bank)
        else:
            self.answer = answer

        print(f"The actual answer is {self.answer} ssssh, dont tell anyone")

        self.past_guesses = []
        self.board = []

        self.board_printer = Console()

        self.ai = ai
    
    def get_word_bank(self):
        return self.word_bank

    def get_past_guesses(self):
        return self.past_guesses
    
    def guess(self):
        valid = False
        while not valid:
            user_guess = input("What is your guess: ")
            user_guess = user_guess.upper()
            if user_guess not in self.word_bank:
                print(f"""
                Oops! Looks like your guess: {guess}, was not found
                in our Word Bank of valid guesses. Please guess again
                """)
            elif len(user_guess) != len(self.answer):
                print(f"""
                Oops! Looks like your guess: {guess}, was not the right 
                length. Expected: {len(self.answer)} Found: {len(guess)}
                """)
            else:
                valid = True

        evaluate_guess(user_guess)
        
    def evaluate_guess(self, user_guess) -> List[Union[str, str]]:
        green_tiles = self.check_for_green_tiles(user_guess)
        yellow_tiles = self.check_for_yellow_tiles(user_guess)

        result = green_tiles + yellow_tiles
        result.sort(key=lambda x: x[2])
        
        # which indices did we miss?
        # these should be marked "grey"
        seen = set()
        grey_tiles = []
        for (_, _, idx) in result:
            seen.add(idx)

        for i in range(len(user_guess)):
            if i not in seen:
                grey_tiles.append(("grey", user_guess[i], i))

        result = result + grey_tiles
        result.sort(key=lambda x: x[2])

        self.past_guesses.append(result)
    
    def check_for_yellow_tiles(self, user_guess: str):
        from collections import Counter
        answer_letters = Counter(self.answer)
        yellow_tiles = []
        for idx in range(len(user_guess)):
            letter = user_guess[idx]

            # yellow tiles cannot be green
            # so skip all tiles which meet 
            # the green condition
            if self.answer[idx] == letter: 
                # 2) decrement counts for green tiles
                answer_letters[letter] -= 1
                continue
            
            # 1) make sure that we do not double count
            elif letter in answer_letters and answer_letters[letter] > 0:
                answer_letters[letter] -= 1
                yellow_tiles.append(("yellow", letter, idx)) 

        return yellow_tiles

    def check_for_green_tiles(self, user_guess: str):
        green_tiles = []
        for idx in range(len(user_guess)):
            if self.answer[idx] == user_guess[idx]:
                green_tiles.append(("green", user_guess[idx], idx))

        return green_tiles

    def render_result(self):
       os.system("clear") 
       if self.ai:
           print(f"You are watching an a.i play")
           print(f"The word it is trying to guess is {self.answer}")

       # paint the rows which have already
       # been guessed 
       for guess_idx, guess in enumerate(self.past_guesses):
           if guess_idx == len(self.past_guesses) - 1:
               delay = .2
           else:
               delay = 0

           for (color, letter, idx) in guess:
               time.sleep(delay)
               if idx == len(self.answer) - 1:
                   end = ""
               else:
                    end = " "

               if color == "yellow":
                  self.board_printer.print(letter, style="bold yellow", end=end)
               elif color == "grey":
                   self.board_printer.print(letter, style="bold #808080", end=end)
               elif color == "green":
                   self.board_printer.print(letter, style="bold green", end=end)
               else:
                   raise Exception(f"Ooops, looks like you did not pass a valid color. \
                                     Should be: [yellow, gray, green] instead found: {color}")
           print()

       if all(color == "green" for color,_, _ in self.past_guesses[-1]):
           print("You win!!!")
           sys.exit()

       if len(self.past_guesses) == 6:
           print("Oops looks like you ran out of guesses. You lose :(")
           sys.exit()
