import logging

import telegram
from telegram import Update
from telegram.error import TelegramError
from telegram.ext import CallbackContext, CommandHandler, Updater

from eliud.conf import settings
from eliud.markups.base import BaseMarkup

logger = logging.getLogger("eliud.telegram")


class Bot:
    """
    Constructs a bot and handles all the interactions
    """

    def __init__(self):
        token = settings.TELEGRAM_TOKEN
        self.bot = telegram.Bot(token=token)
        self.updater = Updater(
            token=token, use_context=True, workers=settings.TELEGRAM_WORKERS
        )
        self.dispatcher = self.updater.dispatcher
        self.commands_descriptions = []

    def add_callback(self, handler, pattern, run_async=False):
        """
        Add Callback action
        :param handler:
        :param pattern:
        :param run_async:
        :return:
        """
        self.dispatcher.add_handler(handler, pattern=pattern, run_async=run_async)

    def add_command(self, command):
        """
        Add command action
        :param command:
        :return:
        """
        self.dispatcher.add_handler(
            CommandHandler(
                command.command, command.get_handle, run_async=command.is_async
            )
        )

        if command.description:
            self.commands_descriptions.append((command.command, command.description))

    def __set_descriptions(self):
        """
        Set commands descriptions in Telegram

        :return:
        """
        self.bot.set_my_commands(self.commands_descriptions)

    def send_message(self, chat_id: str, markup: BaseMarkup):
        try:
            self.bot.send_message(chat_id=chat_id, text=markup.get_text())
        except TelegramError as e:
            logger.error(e)

    def start(self):
        """
        Start the bot in development mode

        """
        self.__set_descriptions()
        self.updater.start_polling()
        self.updater.idle()
        logger.info(f"Running at https://t.me/{self.bot.username}")


def send_message(chat_id: str, markup: BaseMarkup):
    try:
        bot.send_message(chat_id=chat_id, markup=markup)
        return True
    except TelegramError as e:
        logger.error(e)
        return False


bot = Bot()

__all__ = ["bot", "Update", "CallbackContext", "send_message"]
