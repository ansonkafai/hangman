"""Module to define package level functions."""

import random

from hangman.constants import WORDS_LIST


def get_random_word() -> str:
    """Get a random word from the WORDS_LIST constant.

    Returns:
        str: The random word from the WORDS_LIST constant.
    """
    idx = random.randint(0, len(WORDS_LIST) - 1)
    return WORDS_LIST[idx]
