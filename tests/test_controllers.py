"""Module for testing the controller classes."""

from typing import List
from unittest import mock
from unittest.mock import Mock, call

import pytest

from hangman.models import HangmanGameData
from hangman.views import HangmanGameView
from hangman.controllers import HangmanGameController


class TestHangmanGameController:
    """Unit test the controller class HangmanGameController."""

    @pytest.fixture
    def secret_word(self) -> str:
        """Provide default value for game secret_word.

        Returns:
            str: Default value for game secret_word.
        """
        return "one"

    @pytest.fixture
    def correct_letters(self) -> List[str]:
        """Provide default value for game correct_letters.

        Returns:
            List[str]: Default value for game correct_letters.
        """
        return ["o", "n", "e"]

    @pytest.fixture
    def missed_letters(self) -> List[str]:
        """Provide default value for game missed_letters.

        Returns:
            List[str]: Default value for game missed_letters.
        """
        return ["a", "b", "c", "d", "f", "g"]

    @pytest.fixture
    def mock_hangman_game_view(self) -> Mock:
        """Provide mocking object on HangmanGameView.

        Returns:
            Mock: mock object for suppressing UI display and console prompt, and also simulating one round game.
        """

        mock_hangman_game_view = Mock(spec=HangmanGameView)

        # Mock the view object's methods to suppress the UI board display and console prompting.
        mock_hangman_game_view.show_hangman_board.return_value = None
        mock_hangman_game_view.show_player_won.return_value = None
        mock_hangman_game_view.show_player_lost.return_value = None

        # Mock the view object's method to simulate one round only.
        mock_hangman_game_view.play_again.return_value = False

        return mock_hangman_game_view

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

    def test_start_game_one_round_player_win(self, secret_word, correct_letters, mock_hangman_game_view) -> None:
        """Test one round normal flow of Hangman game - player win.

        Args:
            secret_word: The default secret_word from fixture.
            correct_letters: The default correct_letters from fixture.
            mock_hangman_game_view: The default mock on HangmanGameView from fixture.
        """
        # Mock the view object's method to simulate player win normal flow,
        # i.e. returning player guesses exactly same as the secret word.
        mock_hangman_game_view.get_player_guess.side_effect = correct_letters

        # Init game data object and controller, then start the game.
        hangman_game_data = HangmanGameData(secret_word=secret_word)
        hangman_game_controller = HangmanGameController(hangman_game_data, mock_hangman_game_view)
        hangman_game_controller.start_game()

        assert hangman_game_controller.hangman_game_data.correct_letters == correct_letters
        assert hangman_game_controller.hangman_game_data.missed_letters == []
        assert hangman_game_controller.hangman_game_data.game_finished is True

    def test_start_game_one_round_player_lose(self, secret_word, missed_letters, mock_hangman_game_view) -> None:
        """Test one round normal flow of Hangman game - player lose.

        Args:
            secret_word: The default secret_word from fixture.
            missed_letters: The default correct_letters from fixture.
            mock_hangman_game_view: The default mock on HangmanGameView from fixture.
        """
        # Mock the view object's method to simulate player lose normal flow
        # i.e. returning player guesses with no letters match the secret_word.
        mock_hangman_game_view.get_player_guess.side_effect = missed_letters

        # Init game data object and controller, then start the game.
        hangman_game_data = HangmanGameData(secret_word=secret_word)
        hangman_game_controller = HangmanGameController(hangman_game_data, mock_hangman_game_view)
        hangman_game_controller.start_game()

        assert hangman_game_controller.hangman_game_data.correct_letters == []
        assert hangman_game_controller.hangman_game_data.missed_letters == missed_letters
        assert hangman_game_controller.hangman_game_data.game_finished is True

    def test_start_game_two_rounds(self, secret_word, correct_letters, missed_letters, mock_hangman_game_view) -> None:
        """Test two rounds of Hangman game - first round player win, second round player lose.

        Args:
            secret_word: The default secret_word from fixture.
            correct_letters: The default correct_letters from fixture.
            missed_letters: The default correct_letters from fixture.
            mock_hangman_game_view: The default mock on HangmanGameView from fixture.
        """
        # Mock the view object's method to simulate player first round win, second round lose.
        mock_hangman_game_view.get_player_guess.side_effect = correct_letters + missed_letters

        # Mock the view object's method to simulate two rounds.
        mock_hangman_game_view.play_again.side_effect = [True, False]

        # Patch the constant in utils so as to fix the returned random secret word.
        with mock.patch("hangman.utils.WORDS_LIST", [secret_word]):
            # Init game data object and controller, then start the game.
            hangman_game_data = HangmanGameData()
            hangman_game_controller = HangmanGameController(hangman_game_data, mock_hangman_game_view)
            hangman_game_controller.start_game()

            # Assert the first round game,
            # if the view's show_player_won() method is called once with the expected correct_letters.
            hangman_game_data.missed_letters = []
            hangman_game_data.correct_letters = correct_letters
            assert mock_hangman_game_view.show_player_won.mock_calls == [call(hangman_game_data)]

            # Assert the second round game,
            # if the view's show_player_lost() method is called once with the expected missed_letters.
            hangman_game_data.missed_letters = missed_letters
            hangman_game_data.correct_letters = []
            assert mock_hangman_game_view.show_player_lost.mock_calls == [call(hangman_game_data)]
