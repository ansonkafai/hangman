"""Module to define controller classes of the Model-View-Controller design pattern."""

from hangman.constants import HANGMAN_PICS
from hangman.models import HangmanGameData
from hangman.views import HangmanGameView


class HangmanGameController:
    """Controller class of managing Hangman game events."""

    def __init__(
        self,
        hangman_game_data: HangmanGameData = HangmanGameData(),
        hangman_game_view: HangmanGameView = HangmanGameView(),
    ):
        """Control all the events of Hangman game.

        Attributes:
            hangman_game_data: Dataclass object of type HangmanGameData storing the data of the current game.
            hangman_game_view: View object of type HangmanGameView that is responsible for UI display.
        """
        self.hangman_game_data = hangman_game_data
        self.hangman_game_view = hangman_game_view

    def start_game(self) -> None:
        """Start the Hangman game."""
        while True:
            self.hangman_game_view.show_hangman_board(self.hangman_game_data)

            # Let the player enter a guess letter.
            player_guess = self.hangman_game_view.get_player_guess(self.hangman_game_data)

            if player_guess in self.hangman_game_data.secret_word:
                # If guess letter is correct, save it to the correct list.
                self.hangman_game_data.correct_letters.append(player_guess)
                if self.is_player_won():
                    # Check if player won the game, then show winning message.
                    self.hangman_game_view.show_hangman_board(self.hangman_game_data)
                    self.hangman_game_view.show_player_won(self.hangman_game_data)
                    self.hangman_game_data.game_finished = True
            else:
                self.hangman_game_data.missed_letters.append(player_guess)
                if self.is_guessed_too_many_times():
                    # Check if run out of guesses, then show lost game message.
                    self.hangman_game_view.show_hangman_board(self.hangman_game_data)
                    self.hangman_game_view.show_player_lost(self.hangman_game_data)
                    self.hangman_game_data.game_finished = True

            if self.hangman_game_data.game_finished:
                if not self.hangman_game_view.play_again():
                    # Exit the game if player doesn't want to play again.
                    break
                # Refresh the game data if player wants to play again.
                self.hangman_game_data = HangmanGameData()

    def is_player_won(self) -> bool:
        """Check whether the player has won the game."""
        is_player_won = True
        for secret_word_letter in self.hangman_game_data.secret_word:
            if secret_word_letter not in self.hangman_game_data.correct_letters:
                is_player_won = False
                break
        return is_player_won

    def is_guessed_too_many_times(self) -> bool:
        """Check if player has guessed too many times and lost."""
        return len(self.hangman_game_data.missed_letters) >= (len(HANGMAN_PICS) - 1)
