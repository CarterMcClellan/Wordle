from __future__ import annotations

import os, sys, random, time

from rich.console import Console

class Wordle:
    def __init__(
        self,
        answer: str,
        word_bank: list[str],
        ai: bool = False,
        show_answer: bool = True,
    ):
        # check that a list is passed
        if word_bank is None:
            raise Exception("You must provide a valid Word Bank")
        
        # check that the len of all words in the word bank are the same
        expected_len = len(word_bank[0])
        for word in word_bank:
            if len(word) != expected_len:
                raise Exception(
                    f"""Expected all words in word bank to be of len 
                    {expected_len}, instead found {word} (len= {len(word)}"
                    """
                )

        self.word_bank = word_bank
        
        # Validate chosen answer.
        # If an answer is not provided then randomly select
        # an answer from the word bank
        if answer is None:
            self.answer = random.choice(word_bank)
        else:
            self.answer = answer

            if self.answer not in self.word_bank:
                raise Exception(
                    f"""Expected user to pass word in word bank.
                    {self.answer} does not exist in the word bank.
                    """
                )
        
        # Make it optional for users to see the answer
        if show_answer:
            print(f"The actual answer is {self.answer} ssssh, dont tell anyone")
        
        # List of all past guesses
        self.past_guesses = []
        
        # Boolean to indicate whether a human is playing or an ai
        # is playing. If an a.i is playing, then we render the output
        # slightly differently
        self.ai = ai
        
        # Object from 'Rich' python library, which we use to render
        # the board
        self.board_printer = Console()

    def guess(self) -> None:
        """ method which prompts user to make a guess """
        valid = False
        while not valid:
            user_guess = input("What is your guess: ")
            user_guess = user_guess.upper()
            if user_guess not in self.word_bank:
                print(
                    f"""
                Oops! Looks like your guess: {guess}, was not found
                in our Word Bank of valid guesses. Please guess again
                """
                )
            else:
                valid = True

        evaluate_guess(user_guess)

    def get_word_bank(self) -> list[str]:
        """ method which returns word bank """

        raise NotImplementedError("you need to implement this method")

    def get_past_guesses(self) -> list[tuple(str)]:
        """ method which returns past guesses"""

        raise NotImplementedError("you need to implement this method")

    def evaluate_guess(self, user_guess) -> None:
        """
        method which evaluates the users guess.
        should do 2 things

        1) determine which letters are grey, yellow, and green
        2) append those letters (in order) as a list of tuples to past guesses

        Edge Cases to think about:
        
        - Suppose the answer is "STUCK" and your guess is "OASIS".
          The first "S" should be yellow but the second "S" should be
          grey (to indicate that there is only 1 "S" in the answer)

        - Similarly suppose the answer is "CRANE" and your guess is 
          "CROCK" the first "C" should be green and the second should be
          grey.

        Why are these edge cases important?
        
        - It means your functions "check_for_grey_tiles", "check_for_green_tiles"
          and "check_for_yellow_tiles" are not independent! If the letter appears
          in the answer once but the guess twice, and you have already marked it 
          yellow once, then your list of grey tiles must include it. (see example
          above).
        """

        raise NotImplementedError("you need to implement this method")
    
    def check_for_grey_tiles(self, user_guess: str) -> list[tuple(str, str, int)]:
        """
        method which returns all letters in the user guess which are
        NOT in the word!

        note:
            you must return a list of tuples. each tuple must be exactly 3 
            elements long. (color, letter, idx), eg. ("grey", "A", 0)
        """

        raise NotImplementedError("you need to implement this method")

    def check_for_yellow_tiles(self, user_guess: str) -> list[tuple(str, str, int)]:
        """
        method which returns all letters in the user's guess which are
        in the word but are in a DIFFERENT position

        note:
            you must return a list of tuples. each tuple must be exactly 3 
            elements long. (color, letter, idx), eg. ("yellow", "A", 0)
        """

        raise NotImplementedError("you need to implement this method")

    def check_for_green_tiles(self, user_guess: str) -> list[tuple(str, str, int)]:
        """
        method which returns all letters in the user guess which are
        in the word and are in the SAME position

        note:
            you must return a list of tuples. each tuple must be exactly 3 
            elements long. (color, letter, idx), eg. ("green", "A", 0)
        """

        raise NotImplementedError("you need to implement this method")

    def render_result(self) -> None:
        """Method which renders the current wordle board (ignore this)"""

        os.system("clear")
        if self.ai:
            print(f"You are watching an a.i play")
            print(f"The word it is trying to guess is {self.answer}")

        for guess_idx, guess in enumerate(self.past_guesses):
            if guess_idx == len(self.past_guesses) - 1:
                delay = 0.2
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
                    raise Exception(
                        f"Ooops, looks like you did not pass a valid color. \
                                     Should be: [yellow, grey, green] instead found: {color}"
                    )
            print()

        if all(color == "green" for color, _, _ in self.past_guesses[-1]):
            print("You win!!!")
            sys.exit()

        if len(self.past_guesses) == 6:
            print("Oops looks like you ran out of guesses. You lose :(")
            sys.exit()
