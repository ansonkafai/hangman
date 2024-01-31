"""Module to define package level constants."""

import os
from typing import Final, List

HANGMAN_PICS: Final[list] = [
    """
    +---+
        |
        |
        |
       ===""",
    """
    +---+
    O   |
        |
        |
       ===""",
    """
    +---+
    O   |
    |   |
        |
       ===""",
    """
    +---+
    O   |
   /|   |
        |
       ===""",
    """
    +---+
    O   |
   /|\\  |
        |
       ===""",
    """
    +---+
    O   |
   /|\\  |
   /    |
       ===""",
    """
    +---+
    O   |
   /|\\  |
   / \\  |
       ===""",
]

WORDS_SOURCE_DIR: str = os.path.dirname(os.path.abspath(__file__))

WORDS_SOURCE_FILENAME = "words_source.txt"

WORDS_SOURCE_PATH = f"{WORDS_SOURCE_DIR}/{WORDS_SOURCE_FILENAME}"

# Get a list of secret words from the words source text file in current dir.
WORDS_LIST: List[str] = []
with open(WORDS_SOURCE_PATH, mode="r", encoding="utf-8") as words_file:
    lines = words_file.readlines()
    for line in lines:
        WORDS_LIST.extend(line.split())
