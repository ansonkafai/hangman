"""Module for testing the controller classes."""

from hangman.models import HangmanGameData
from hangman.controllers import HangmanGameController


class TestHangmanGameController:
    """Unit test the controller class HangmanGameController."""

    def test_is_player_won_true(self) -> None:
        """Test positive case of the is_player_won() method of HangmanGameController."""
        hangman_game_data = HangmanGameData(secret_word="test", correct_letters=["t", "e", "s", "t"])
        hangman_game_controller = HangmanGameController(hangman_game_data)
        assert hangman_game_controller.is_player_won() is True

    def test_is_player_won_false(self) -> None:
        """Test negative case of the is_player_won() method of HangmanGameController."""
        hangman_game_data = HangmanGameData(secret_word="test", correct_letters=["e", "s"])
        hangman_game_controller = HangmanGameController(hangman_game_data)
        assert hangman_game_controller.is_player_won() is False

    def test_is_guessed_too_many_times_true(self) -> None:
        """Test positive case of the is_guessed_too_many_times() method of HangmanGameController."""
        hangman_game_data = HangmanGameData(missed_letters=["a", "b", "c", "d", "e", "f"])
        hangman_game_controller = HangmanGameController(hangman_game_data)
        assert hangman_game_controller.is_guessed_too_many_times() is True

        hangman_game_data.missed_letters.append("g")
        assert hangman_game_controller.is_guessed_too_many_times() is True

    def test_is_guessed_too_many_times_false(self) -> None:
        """Test negative case of the is_guessed_too_many_times() method of HangmanGameController."""
        hangman_game_data = HangmanGameData(missed_letters=["a"])
        hangman_game_controller = HangmanGameController(hangman_game_data)
        assert hangman_game_controller.is_guessed_too_many_times() is False
