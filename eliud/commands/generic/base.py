import logging
import re

from ..exceptions import CommandException

logger = logging.getLogger("eliud.command")


def _validate_command(command: str):
    command = command.split("?")[0]
    match = re.fullmatch("[a-zA-Z]+[a-zA-Z0-9-_]*", command)
    if not match:
        raise CommandException(f"Command {command} is not a valid command")


class BaseCommand:
    def __init__(self, **kwargs):
        """
        Constructor. Called in the CommandConf; can contain helpful extra
        keyword arguments, and other things.
        """
        # Go through keyword arguments, and either save their values to our
        # instance, or raise an error.
        for key, value in kwargs.items():
            if key == "command":
                _validate_command(value)
            setattr(self, key, value)


class Command(BaseCommand):
    command: str = None
    markup = None
    markup_kwargs: dict = None

    def render_markup(self, **kwargs):
        return self.markup(**kwargs)
