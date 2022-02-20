import os
from abc import ABC
from enum import Enum
from typing import List

from xtermcolor import colorize


class Score(Enum):
    BLANK = 0
    INCORRECT = 1
    INCORRECT_POSITION = 2
    CORRECT = 3


class Renderer(ABC):
    """
    Abstract class that contains rendering logic.
    Subclass this to a concrete class definition.
    """

    def __init__(self, length: int, attempts: int) -> None:
        self.title = self._render_title(length=length)
        self.board = [self._char_blank() * length] * attempts
        self.guesses: List[str] = []
        self.attempt = 0

    def _render_title(self, length: int):
        raise NotImplementedError()

    def _print_guesses(self):
        if self.guesses:
            print("Previous guesses:")
            for guess in self.guesses:
                print(guess)
            print("\n")

    def _clear_output(self):
        os.system("cls" if os.name == "nt" else "printf '\033c'")

    def _char_blank(self):
        raise NotImplementedError()

    def _char_incorrect(self, char: str):
        raise NotImplementedError()

    def _char_incorrect_position(self, char: str):
        raise NotImplementedError()

    def _char_correct(self, char: str):
        raise NotImplementedError()

    def render_board(self):
        self._clear_output()
        print(self.title)
        for row in self.board:
            print(row)

    def update_board(self, guesses: List[str], scores: List[List[Score]]):
        """
        Lazily renders the latest guess and score only,
        instead of re-rendering the entire board

        Args:
            guesses (List[str]): List of all valid guesses to date
            scores (List[List[Score]]): List of List[Score], corresponding to guesses
        """
        row = ""
        self.guesses = guesses
        for char, score in zip(guesses[-1], scores[-1]):
            if score == Score.INCORRECT:
                row += self._char_incorrect(char)
            elif score == Score.INCORRECT_POSITION:
                row += self._char_incorrect_position(char)
            else:
                row += self._char_correct(char)
        self.board[self.attempt] = row
        self.attempt += 1

        self.render_board()


class AsciiRenderer(Renderer):
    """
    Renderer that uses ASCII characters to show progress.
    """

    HEX_WHITE = 0xFFFFFF
    HEX_GREY = 0x3C3C3E
    HEX_YELLOW = 0xAD9E45
    HEX_GREEN = 0x688C52

    def _char_blank(self):
        return colorize("___", rgb=self.HEX_WHITE, bg=self.HEX_WHITE)

    def _char_incorrect(self, char: str):
        return colorize(f" {char} ", rgb=self.HEX_WHITE, bg=self.HEX_GREY)

    def _char_incorrect_position(self, char: str):
        return colorize(f" {char} ", rgb=self.HEX_WHITE, bg=self.HEX_YELLOW)

    def _char_correct(self, char: str):
        return colorize(f" {char} ", rgb=self.HEX_WHITE, bg=self.HEX_GREEN)

    def _render_title(self, length: int):
        return "pyWORDLE".center(length * 3)


class EmojiRenderer(Renderer):
    """
    Renderer that uses emoji squares to show progress.
    Overrides render_board() to also include guess history.
    """

    def _char_blank(self):
        return "⬜"

    def _char_incorrect(self, char: str):
        return "⬛"

    def _char_incorrect_position(self, char: str):
        return "🟨"

    def _char_correct(self, char: str):
        return "🟩"

    def _render_title(self, length: int):
        return "pyWORDLE".center(length * 2)

    def render_board(self):
        super().render_board()
        self._print_guesses()
