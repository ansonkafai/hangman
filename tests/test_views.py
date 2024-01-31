"""Module for testing the views module."""

from unittest import mock

from hangman.models import HangmanGameData
from hangman.constants import HANGMAN_PICS
from hangman.views import (
    validate_player_guess,
    play_again,
    get_player_guess,
    get_hangman_pic,
    get_player_won_message,
    get_player_lost_message_first_line,
    get_player_lost_message_second_line,
)


class TestUtils:
    """Unit test the views module."""

    def test_validate_player_guess_entered_more_than_one_letter(self) -> None:
        """Test the validate_player_guess() method of views module, entered more than one letter."""
        input_letter = "ab"
        hangman_game_data = HangmanGameData(player_guess=input_letter)
        input_err, err_msg = validate_player_guess(hangman_game_data)
        assert input_err is True
        assert err_msg == "Please enter one letter only."

    def test_validate_player_guess_entered_letter_already_guessed(self) -> None:
        """Test the validate_player_guess() method of views module, entered letter that already guessed."""
        input_letter = "a"
        hangman_game_data = HangmanGameData(player_guess=input_letter, missed_letters=[input_letter])
        input_err, err_msg = validate_player_guess(hangman_game_data)
        assert input_err is True
        assert err_msg == f"You have already guessed the letter [{input_letter}]. Please choose again."

    def test_validate_player_guess_entered_letter_not_alphabet(self) -> None:
        """Test the validate_player_guess() method of views module, entered letter is not an alphabet."""
        input_letter = "3"
        hangman_game_data = HangmanGameData(player_guess=input_letter)
        input_err, err_msg = validate_player_guess(hangman_game_data)
        assert input_err is True
        assert err_msg == "Please enter an alphabet letter (a-z/A-Z)."

    def test_get_player_guess(self) -> None:
        """Test normal case of the get_player_guess() method of views module."""
        input_letter = "a"
        with mock.patch("click.prompt") as mock_prompt:
            mock_prompt.return_value = input_letter
            assert get_player_guess(HangmanGameData()) == input_letter

    def test_play_again_true(self) -> None:
        """Test normal case of the get_random_word() method of views module."""
        with mock.patch("click.prompt") as mock_prompt:
            mock_prompt.return_value = "y"
            assert play_again() is True

    def test_play_again_false(self) -> None:
        """Test negative cases of the get_random_word() method of views module."""
        with mock.patch("click.prompt") as mock_prompt:
            mock_prompt.return_value = "n"
            assert play_again() is False
            mock_prompt.return_value = "a"
            assert play_again() is False

    def test_get_hangman_pic(self) -> None:
        """Test the get_hangman_pic() method of views module.

        Check if Hangman pic retrieved correctly according to the number of missed guesses.
        """
        hangman_game_data = HangmanGameData(missed_letters=["a", "b"])
        assert get_hangman_pic(hangman_game_data) == HANGMAN_PICS[len(hangman_game_data.missed_letters)]

    def test_get_player_won_message(self) -> None:
        """Test the get_player_won_message() method of views module."""
        hangman_game_data = HangmanGameData(secret_word="test")
        expected_msg = f"You won the game! The secret word is '{hangman_game_data.secret_word}'."
        assert get_player_won_message(hangman_game_data) == expected_msg

    def test_get_player_lost_message_first_line(self) -> None:
        """Test the get_player_lost_message_first_line() method of views module."""
        hangman_game_data = HangmanGameData(secret_word="test")
        expected_msg = f"You have run out of guesses! The word is: '{hangman_game_data.secret_word}'."
        assert get_player_lost_message_first_line(hangman_game_data) == expected_msg

    def test_get_player_lost_message_second_line(self) -> None:
        """Test the get_player_lost_message_second_line() method of views module."""
        missed_letters = ["a", "b", "c", "d", "f", "g"]
        correct_letters = ["e"]
        hangman_game_data = HangmanGameData(
            secret_word="test", missed_letters=missed_letters, correct_letters=correct_letters
        )
        expected_msg = f"Score: missed guesses=[{len(missed_letters)}], correct guess=[1]."
        assert get_player_lost_message_second_line(hangman_game_data) == expected_msg

        correct_letters = ["e", "s"]
        hangman_game_data.correct_letters = correct_letters
        expected_msg = f"Score: missed guesses=[{len(missed_letters)}], correct guesses=[{len(correct_letters)}]."
        assert get_player_lost_message_second_line(hangman_game_data) == expected_msg
