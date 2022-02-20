"""Main game module"""
import random
from datetime import date
from typing import Callable, List

from renderer import AsciiRenderer, EmojiRenderer, Renderer, Score
from words import load_words


class PyWordle:
    """
    Create an instance of this class and call .start_game()
    """

    def __init__(
        self, length: int = 5, attempts: int = 6, renderer: Callable = AsciiRenderer
    ) -> None:
        """
        Args:
            length (int, optional): Word length. Defaults to 5.
            attempts (int, optional): Number of attempts allowed. Defaults to 6.
            renderer (Callable, optional): Renderer subclass which controls
                how game board is displayed. Defaults to AsciiRenderer.
        """
        self._length = length
        self._attempts = attempts
        self._renderer: Renderer = renderer(length=length, attempts=attempts)
        self._words = load_words(length=length)
        self._guesses: List[str] = []
        self._scores: List[List[Score]] = []
        self._answer = self._choose_word()

    def _choose_word(self, seed: int = date.today().toordinal()) -> str:
        """
        Internal method to choose the secret word.
        Uses the current day as a default seed.

        Args:
            seed (int, optional): Defaults to date.today().toordinal().

        Returns:
            str: Secret word.
        """
        random.seed(seed)
        return random.choice(self._words).upper()

    def start_game(self):
        self._renderer.render_board()

        for _ in range(self._attempts):
            self._guesses.append(self._input_guess())
            self._scores.append(self._scorer(guess=self._guesses[-1]))

            self._renderer.update_board(guesses=self._guesses, scores=self._scores)
            if self._guesses[-1] == self._answer:
                print(f"You guessed the answer: {self._answer}!")
                return
        print(f"You failed to guess the answer: {self._answer}!")

    def reset_game(self):
        """
        Resets game state.
        Answer is not changed.
        """
        self._guesses = []
        self._scores = []
        self.start_game()

    def _scorer(self, guess: str) -> List[Score]:
        """
        Scores user's guess against self._answer

        Args:
            guess (str): User supplied guess

        Returns:
            List[Score]: List of Score objects.
        """

        score = []

        for idx, letter in enumerate(guess):
            if letter.upper() == self._answer[idx]:
                score.append(Score.CORRECT)
            elif letter.upper() in self._answer.upper():
                score.append(Score.INCORRECT_POSITION)
            else:
                score.append(Score.INCORRECT)
        return score

    def _input_guess(self) -> str:

        while True:
            guess = input("Type a guess:\n").upper()
            if not guess.isalpha():
                print(f"{guess} is not an alphabetic guess. Try again")
            elif (guess_len := len(guess)) != self._length:
                print(
                    f"Your guess must be {self._length} letters long (was {guess_len}). Try again."
                )
            elif guess not in self._words:
                print(f"{guess} is not a valid word. Try again.")
            else:
                return guess


if __name__ == "__main__":
    # board = PyWordle(renderer=AsciiRenderer)
    board = PyWordle(renderer=EmojiRenderer)
    board.start_game()
