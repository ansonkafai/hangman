"""Module for testing the views module."""

from unittest import mock
import pytest

from hangman.models import HangmanGameData
from hangman.constants import HANGMAN_PICS
from hangman.views import HangmanGameView


class TestHangmanGameView:
    """Unit test the HangmanGameView class."""

    @pytest.fixture
    def under_test(self) -> HangmanGameView:
        """Provide HangmanGameView object as a fixture for the subsequent unit tests.

        Returns:
            HangmanGameView: The object to be tested.
        """
        return HangmanGameView()

    def test_validate_player_guess_entered_more_than_one_letter(self, under_test: HangmanGameView) -> None:
        """Test the validate_player_guess() method of HangmanGameView class, entered more than one letter.

        Args:
            under_test: The to-be-tested HangmanGameView object from fixture.
        """
        input_letter = "ab"
        hangman_game_data = HangmanGameData(player_guess=input_letter)
        input_err, err_msg = under_test.validate_player_guess(hangman_game_data)
        assert input_err is True
        assert err_msg == "Please enter one letter."

    def test_validate_player_guess_entered_letter_already_guessed(self, under_test: HangmanGameView) -> None:
        """Test the validate_player_guess() method of HangmanGameView class, entered letter that already guessed.

        Args:
            under_test: The to-be-tested HangmanGameView object from fixture.
        """
        input_letter = "a"
        hangman_game_data = HangmanGameData(player_guess=input_letter, missed_letters=[input_letter])
        input_err, err_msg = under_test.validate_player_guess(hangman_game_data)
        assert input_err is True
        assert err_msg == f"You have already guessed the letter [{input_letter}]. Please choose again."

    def test_validate_player_guess_entered_letter_not_alphabet(self, under_test: HangmanGameView) -> None:
        """Test the validate_player_guess() method of HangmanGameView class, entered letter is not an alphabet.

        Args:
            under_test: The to-be-tested HangmanGameView object from fixture.
        """
        input_letter = "3"
        hangman_game_data = HangmanGameData(player_guess=input_letter)
        input_err, err_msg = under_test.validate_player_guess(hangman_game_data)
        assert input_err is True
        assert err_msg == "Please enter an alphabet letter (a-z/A-Z)."

    def test_get_player_guess(self, under_test: HangmanGameView) -> None:
        """Test normal case of the get_player_guess() method of HangmanGameView class.

        Args:
            under_test: The to-be-tested HangmanGameView object from fixture.
        """
        input_letter = "a"
        with mock.patch("click.prompt") as mock_prompt:
            mock_prompt.return_value = input_letter
            assert under_test.get_player_guess(HangmanGameData()) == input_letter

    def test_play_again_true(self, under_test: HangmanGameView) -> None:
        """Test normal case of the get_random_word() method of HangmanGameView class.

        Args:
            under_test: The to-be-tested HangmanGameView object from fixture.
        """
        with mock.patch("click.prompt") as mock_prompt:
            mock_prompt.return_value = "y"
            assert under_test.play_again() is True

    def test_play_again_false(self, under_test: HangmanGameView) -> None:
        """Test negative cases of the get_random_word() method of HangmanGameView class.

        Args:
            under_test: The to-be-tested HangmanGameView object from fixture.
        """
        with mock.patch("click.prompt") as mock_prompt:
            mock_prompt.return_value = "n"
            assert under_test.play_again() is False
            mock_prompt.return_value = "a"
            assert under_test.play_again() is False

    def test_get_hangman_pic(self, under_test: HangmanGameView) -> None:
        """Test the get_hangman_pic() method of HangmanGameView class.

        Check if Hangman pic retrieved correctly according to the number of missed guesses.

        Args:
            under_test: The to-be-tested HangmanGameView object from fixture.
        """
        hangman_game_data = HangmanGameData(missed_letters=["a", "b"])
        assert under_test.get_hangman_pic(hangman_game_data) == HANGMAN_PICS[len(hangman_game_data.missed_letters)]

    def test_get_player_won_message(self, under_test: HangmanGameView) -> None:
        """Test the get_player_won_message() method of HangmanGameView class.

        Args:
            under_test: The to-be-tested HangmanGameView object from fixture.
        """
        hangman_game_data = HangmanGameData(secret_word="test")
        expected_msg = f"You won the game! The word is '{hangman_game_data.secret_word}'."
        assert under_test.get_player_won_message(hangman_game_data) == expected_msg

    def test_get_player_lost_message_first_line(self, under_test: HangmanGameView) -> None:
        """Test the get_player_lost_message_first_line() method of HangmanGameView class.

        Args:
            under_test: The to-be-tested HangmanGameView object from fixture.
        """
        hangman_game_data = HangmanGameData(secret_word="test")
        expected_msg = f"You have run out of guesses! The word is: '{hangman_game_data.secret_word}'."
        assert under_test.get_player_lost_message_first_line(hangman_game_data) == expected_msg

    def test_get_player_lost_message_second_line(self, under_test: HangmanGameView) -> None:
        """Test the get_player_lost_message_second_line() method of HangmanGameView class.

        Args:
            under_test: The to-be-tested HangmanGameView object from fixture.
        """
        missed_letters = ["a", "b", "c", "d", "f", "g"]
        correct_letters = ["e"]
        hangman_game_data = HangmanGameData(
            secret_word="test", missed_letters=missed_letters, correct_letters=correct_letters
        )
        expected_msg = f"Score: missed guesses=[{len(missed_letters)}], correct guess=[1]."
        assert under_test.get_player_lost_message_second_line(hangman_game_data) == expected_msg

        correct_letters = ["e", "s"]
        hangman_game_data.correct_letters = correct_letters
        expected_msg = f"Score: missed guesses=[{len(missed_letters)}], correct guesses=[{len(correct_letters)}]."
        assert under_test.get_player_lost_message_second_line(hangman_game_data) == expected_msg

    def test_get_missed_letters_message(self, under_test: HangmanGameView) -> None:
        """Test the get_missed_letters_message() method of HangmanGameView class.

        Args:
            under_test: The to-be-tested HangmanGameView object from fixture.
        """
        hangman_game_data = HangmanGameData(missed_letters=["t", "e"])
        expected_msg = f"Missed letters : {' '.join(hangman_game_data.missed_letters)}"
        assert under_test.get_missed_letters_message(hangman_game_data) == expected_msg

    def test_get_secret_word_with_correct_letters_message(self, under_test: HangmanGameView) -> None:
        """Test the get_secret_word_with_correct_letters_message() method of HangmanGameView class.

        Args:
            under_test: The to-be-tested HangmanGameView object from fixture.
        """
        hangman_game_data = HangmanGameData(secret_word="camel", correct_letters=["a", "e", "m"])
        expected_msg = "Correct letters: _ a m e _"
        assert under_test.get_secret_word_with_correct_letters_message(hangman_game_data) == expected_msg
