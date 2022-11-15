import logging

from telegram.error import TelegramError

from eliud.markups.base import BaseMarkup

from . import bot

logger = logging.getLogger("eliud.telegram")


def send_message(chat_id: str, markup: BaseMarkup):
    try:
        bot.send_message(chat_id=chat_id, text=markup)
        return True
    except TelegramError as e:
        logger.error(e)
        return False
