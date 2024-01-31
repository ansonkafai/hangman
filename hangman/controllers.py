"""Module to define controller classes of the Model-View-Controller design pattern."""

from hangman.constants import HANGMAN_PICS
from hangman.models import HangmanGameData
from hangman.views import get_player_guess, play_again, show_hangman_board, show_player_lost, show_player_won


class HangmanGameController:
    """Controller class of managing Hangman game events."""

    def __init__(self, hangman_game_data: HangmanGameData = HangmanGameData()):
        """Control all the events of Hangman game.

        Attributes:
            hangman_game_data: Dataclass object of type HangmanGameData storing the data of the current game.
        """
        self.hangman_game_data = hangman_game_data

    def start_game(self):
        """Start the Hangman game."""
        while True:
            show_hangman_board(self.hangman_game_data)

            # Let the player enter a guess letter.
            player_guess = get_player_guess(self.hangman_game_data)

            if player_guess in self.hangman_game_data.secret_word:
                # If guess letter is correct, save it to the correct list.
                self.hangman_game_data.correct_letters.append(player_guess)
                if self.is_player_won():
                    # Check if player won the game, show winning message.
                    show_hangman_board(self.hangman_game_data)
                    show_player_won(self.hangman_game_data)
                    self.hangman_game_data.game_finished = True
            else:
                self.hangman_game_data.missed_letters.append(player_guess)
                if self.is_guessed_too_many_times():
                    # Check if run out of guesses, show lost game message.
                    show_hangman_board(self.hangman_game_data)
                    show_player_lost(self.hangman_game_data)
                    self.hangman_game_data.game_finished = True

            if self.hangman_game_data.game_finished:
                if play_again():
                    # Refresh the game data if player wants to play again.
                    self.hangman_game_data = HangmanGameData()
                else:
                    break

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
