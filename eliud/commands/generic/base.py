import logging
import re
from typing import Type

from eliud.commands.exceptions import CommandException
from eliud.markups.base import Markup

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
    markup: Type[Markup] = None
    markup_kwargs: dict = None

    def __init__(self, **kwargs):
        super(Command, self).__init__(**kwargs)
        if not self.command:
            try:
                self.command = kwargs.pop("command")
            except KeyError:
                raise AttributeError("You must provide a 'command' string")

        if not self.markup:
            try:
                self.markup = kwargs.pop("markup")
            except KeyError:
                raise AttributeError("You must provide a markup")

    def render_markup(self, **kwargs):
        return self.markup(**kwargs)
