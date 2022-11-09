import logging
import re

from ..exceptions import CommandException

logger = logging.getLogger("eliud.command")


def _validate_command(command: str):
    match = re.fullmatch("[a-zA-Z]+[a-zA-Z0-9]", command)
    if not match:
        raise CommandException(f"Command {command} is not a valid command")


class Command:
    def __init__(self, command: str):
        _validate_command(command)
        self.command = command
