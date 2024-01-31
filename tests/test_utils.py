"""Module for testing the utils module."""

from unittest import mock

from hangman.utils import get_random_word


class TestUtils:  # pylint: disable=too-few-public-methods
    """Unit test the utils module."""

    def test_get_random_word(self) -> None:
        """Test the get_random_word() method of utils module."""
        expected_word = "one"
        with mock.patch("hangman.utils.WORDS_LIST", [expected_word]):
            assert get_random_word() == expected_word
