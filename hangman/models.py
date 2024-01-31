"""Module to define model classes of the Model-View-Controller design pattern."""

from dataclasses import dataclass, field
from typing import List

from hangman.utils import get_random_word


@dataclass
class HangmanGameData:
    """Represent the information of a Hangman game.

    Reasons of using dataclass:
    (1) Less boilerplate code.
    (2) More readability and better code maintainability.

    Attributes:
        player_guess: (str) The current letter guessed by player.
        secret_word: (str) Random generated secret word of the current game.
        missed_letters: (List[str]) List of missed letters of the current game.
        correct_letters: (List[str]) List of correct letters of the current game.
        game_finished: (bool) Game finish indicator.
    """

    player_guess: str = field(default="")
    secret_word: str = field(default_factory=get_random_word)
    missed_letters: List[str] = field(default_factory=list)
    correct_letters: List[str] = field(default_factory=list)
    game_finished: bool = field(default=False)

    @property
    def already_guessed_letters(self) -> List[str]:
        """Get all letters that have been guessed by the player.

        Returns:
            list[str]: A list combining the elements of missed letters and correct letters. Duplicates are removed.
        """
        return list(set(self.missed_letters + self.correct_letters))

    @property
    def secret_word_with_correct_letters(self) -> str:
        """Combining the secret word with correct guessed letters.

        Returns:
            str: E.g. secret word is 'camel', correct guessed letters are 'a, e, m', then result will be '_ a m e _'.
        """
        blanks = "_" * len(self.secret_word)

        # Replace blanks with correctly guessed letters.
        for idx, secret_word_letter in enumerate(self.secret_word):
            if secret_word_letter in self.correct_letters:
                blanks = f"{blanks[:idx]}{secret_word_letter}{blanks[idx + 1:]}"

        # Return the secret word with spaces in between each letter.
        return " ".join(blanks)
