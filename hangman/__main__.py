"""Default module and the entry point of the package."""

import sys

import click
from click.exceptions import Abort
from hangman.controllers import HangmanGameController

ERR_MSG_GAME_TERMINATED = "Game terminated by player."

try:
    controller = HangmanGameController()
    controller.start_game()
except KeyboardInterrupt:
    click.echo()
    click.secho(ERR_MSG_GAME_TERMINATED, fg="bright_red")
    sys.exit(1)
except Abort:
    click.echo()
    click.secho(ERR_MSG_GAME_TERMINATED, fg="bright_red")
    sys.exit(1)
