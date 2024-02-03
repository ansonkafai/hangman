"""Module to define view functions of the Model-View-Controller design pattern."""

from typing import Tuple

import click

from hangman.constants import HANGMAN_PICS
from hangman.models import HangmanGameData


class HangmanGameView:
    """View class of Hangman game."""

    def clear_screen(self) -> None:
        """Clear console. Just in case we need to change the way of clearing screen."""
        click.clear()

    def validate_player_guess(self, hangman_game_data: HangmanGameData) -> Tuple[bool, str]:
        """Validate guess letter entered by player.

        Args:
            hangman_game_data: HangmanGameData data object for getting the guess letter and already_guessed_letters.

        Returns:
            bool, str: The bool indicates if the input letter is invalid. The str is the error message respectively.
        """
        input_err, err_msg = False, ""
        guess_letter = hangman_game_data.player_guess

        if len(guess_letter) != 1:
            input_err, err_msg = True, "Please enter one letter only."
        elif guess_letter in hangman_game_data.already_guessed_letters:
            input_err, err_msg = True, f"You have already guessed the letter [{guess_letter}]. Please choose again."
        elif not guess_letter.isalpha():
            input_err, err_msg = True, "Please enter an alphabet letter (a-z/A-Z)."

        return input_err, err_msg

    def get_player_guess(self, hangman_game_data: HangmanGameData) -> str:
        """Get the letter the player entered. It makes sure the player entered a single alphabet letter.

        Args:
            hangman_game_data: The data object for retrieving the already guessed letters to prevent duplicate guess.

        Returns:
            str: The guess letter entered by the player.
        """
        input_err = False
        while True:
            if not input_err:
                # Print a blank line in order to fix the position of the subsequent strings.
                click.secho()

            # Capture and validate player's input.
            hangman_game_data.player_guess = click.prompt("Please enter a guess letter").lower()
            input_err, err_msg = self.validate_player_guess(hangman_game_data)

            if input_err:
                # On input error, refresh the board so that the error message can always be displayed on the fixed line.
                self.show_hangman_board(hangman_game_data)
                click.secho(err_msg, fg="bright_red")
            else:
                # Otherwise the guess was captured, we can then exit the loop and function.
                break

        return hangman_game_data.player_guess

    def play_again(self) -> bool:
        """Ask if player wants to play again.

        Returns:
            bool: True if the player wants to play again, and vice versa.
        """
        return click.prompt("Do you want to play again? [y/n]").lower().startswith("y")

    def show_hangman_board_title(self) -> None:
        """Show Hangman board title to console."""
        click.secho(" H A N G M A N ", fg="white", bg="green", bold=True)

    def get_hangman_pic(self, hangman_game_data: HangmanGameData) -> str:
        """Get Hangman picture according to the number of missed guesses.

        Args:
            hangman_game_data: The data object for retrieving the number of missed letters.

        Returns:
            str: The Hangman picture.
        """
        return HANGMAN_PICS[len(hangman_game_data.missed_letters)]

    def show_hangman_pic(self, hangman_game_data: HangmanGameData) -> None:
        """Show Hangman picture to console according to the number of missed guesses.

        Args:
            hangman_game_data: The data object for retrieving the number of missed letters.
        """
        click.secho(self.get_hangman_pic(hangman_game_data), fg="bright_red", bold=True)

    def get_missed_letters_message(self, hangman_game_data: HangmanGameData) -> str:
        """Get missed letters message.

        Args:
            hangman_game_data: The data object for retrieving the missed letters.
        """
        return f"Missed letters : {' '.join(hangman_game_data.missed_letters)}"

    def show_missed_letters(self, hangman_game_data: HangmanGameData) -> None:
        """Show missed guesses to console.

        Args:
            hangman_game_data: The data object for retrieving the missed letters.
        """
        click.secho(self.get_missed_letters_message(hangman_game_data))

    def get_secret_word_with_correct_letters_message(self, hangman_game_data: HangmanGameData) -> str:
        """Get correct guesses message.

        Args:
            hangman_game_data: The data object for retrieving the combination of secret word and correct letters.
        """
        return f"Correct letters: {hangman_game_data.secret_word_with_correct_letters}"

    def show_secret_word_with_correct_letters(self, hangman_game_data: HangmanGameData) -> None:
        """Show correct guesses to console.

        Args:
            hangman_game_data: The data object for retrieving the combination of secret word and correct letters.
        """
        click.secho(self.get_secret_word_with_correct_letters_message(hangman_game_data))

    def show_hangman_board(self, hangman_game_data: HangmanGameData) -> None:
        """Show Hangman board to console.

        Args:
            hangman_game_data: The data object for retrieving the Hangman game data.
        """
        self.clear_screen()
        self.show_hangman_board_title()
        self.show_hangman_pic(hangman_game_data)
        self.show_missed_letters(hangman_game_data)
        self.show_secret_word_with_correct_letters(hangman_game_data)

    def get_player_won_message(self, hangman_game_data: HangmanGameData) -> str:
        """Get player won message.

        Args:
            hangman_game_data: The data object for retrieving the secret word.

        Returns:
            str: The player won message.
        """
        return f"You won the game! The secret word is '{hangman_game_data.secret_word}'."

    def show_player_won(self, hangman_game_data: HangmanGameData) -> None:
        """Show player won message.

        Args:
            hangman_game_data: The data object for retrieving the secret word.
        """
        click.secho(self.get_player_won_message(hangman_game_data), fg="bright_blue")

    def get_player_lost_message_first_line(self, hangman_game_data: HangmanGameData) -> str:
        """Get first line of player lost message.

        Args:
            hangman_game_data: The data object for retrieving the secret word.

        Returns:
            str: The first line of player lost message.
        """
        return f"You have run out of guesses! The word is: '{hangman_game_data.secret_word}'."

    def get_player_lost_message_second_line(self, hangman_game_data: HangmanGameData) -> str:
        """Get second line of player lost message.

        Args:
            hangman_game_data: The data object for retrieving the numbers of missed letters and correct letters.

        Returns:
            str: The second line of player lost message.
        """
        missed_count = len(hangman_game_data.missed_letters)
        correct_count = len(hangman_game_data.correct_letters)
        guess_word_missed = "guesses" if missed_count > 1 else "guess"
        guess_word_correct = "guesses" if correct_count > 1 else "guess"
        return f"Score: missed {guess_word_missed}=[{missed_count}], correct {guess_word_correct}=[{correct_count}]."

    def show_player_lost(self, hangman_game_data: HangmanGameData) -> None:
        """Show player lost message to console.

        Args:
            hangman_game_data: The data object for retrieving the numbers of missed letters and correct letters.
        """
        click.secho(self.get_player_lost_message_first_line(hangman_game_data), fg="bright_red")
        click.secho(self.get_player_lost_message_second_line(hangman_game_data))
