"""Module for testing the model classes."""

from typing import List

import pytest

from hangman.models import HangmanGameData


class TestHangmanGameData:
    """Unit test the model class HangmanGameData."""

    @pytest.fixture
    def missed_letters(self) -> List[str]:
        """Provide missed_letters of the HangmanGameData object for unit testing.

        Returns:
            List[str]: List of missed letters.
        """
        return ["a", "z", "h"]

    @pytest.fixture
    def correct_letters(self) -> List[str]:
        """Provide correct_letters of the HangmanGameData object for unit testing.

        Returns:
            List[str]: List of correct letters.
        """
        return ["e", "s"]

    @pytest.fixture
    def under_test(self, missed_letters: List[str], correct_letters: List[str]) -> HangmanGameData:
        """Provide HangmanGameData object for unit testing.

        Args:
            missed_letters: The missed letters list from predefined fixture.
            correct_letters: The correct letters list from predefined fixture.

        Returns:
            HangmanGameData: The Hangman game data object to be tested.
        """
        return HangmanGameData(secret_word="test", missed_letters=missed_letters, correct_letters=correct_letters)

    def test_already_guessed_letters(
        self, under_test: HangmanGameData, missed_letters: List[str], correct_letters: List[str]
    ) -> None:
        """Test the already_guessed_letters() method of HangmanGameData object.

        Args:
            under_test: The to be tested HangmanGameData object from predefined fixture.
            missed_letters: The missed letters list from predefined fixture.
            correct_letters: The correct letters list from predefined fixture.
        """
        assert under_test.already_guessed_letters == list(set(missed_letters + correct_letters))

    def test_secret_word_with_correct_letters(self, under_test: HangmanGameData) -> None:
        """Test the secret_word_with_correct_letters() method of HangmanGameData object.

        Args:
            under_test: The to be tested HangmanGameData object from predefined fixture.
        """
        assert under_test.secret_word_with_correct_letters == "_ e s _"
