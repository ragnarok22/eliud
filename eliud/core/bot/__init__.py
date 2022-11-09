import logging
from typing import Dict, List, Tuple

from eliud.conf import settings
from eliud.core.exceptions import ImproperlyConfigured

logger = logging.getLogger("eliud.bot")


class Bot:
    def __init__(self, token: str = None):
        if token:
            self.token = token
        else:
            try:
                self.token = getattr(settings, "TELEGRAM_TOKEN")
            except AttributeError:
                raise ImproperlyConfigured(
                    "You must set 'TELEGRAM_TOKEN' in your settings"
                )
        self.__command_descriptions: List[Tuple[str, str]] = []

    def add_command(
        self,
        command_name: str,
        command_func: callable,
        run_async=False,
        description: str = None,
    ):
        """Add a command to bot. If description is provided, this set the command
        to the bot.

        :param command_name: string used to command
        :param command_func: callable to execute the function
        :param run_async: run the command asynchronously
        :param description: set a command description
        """
        # self.dispatcher.add_handler(
        #     CommandHandler(command_name, command_func, run_async=run_async)
        # )
        if description:
            self.__command_descriptions.append((command_name, description))

    def add_callback(self, callback: callable, pattern: str, run_async=False):
        """
        Add a callback action from button.

        :param callback: a callback to execute
        :param pattern: pattern receive
        :param run_async: run the callback asynchronously
        :return: None
        """
        # self.dispatcher.add_handler(
        #     CallbackQueryHandler(
        #         callback, pattern=pattern, run_async=run_async
        #     )
        # )

    def add_conversation(
        self, entry_points: List[Tuple[callable, str]], states: Dict, fallbacks: List
    ):
        """
        Add a conversation handler.

        :param entry_points: entry point for conversation
        :param states: conversation states
        :param fallbacks: fallbacks
        :return: None
        """
        # self.dispatcher.add_handler(
        #     ConversationHandler(
        #         entry_points=[
        #             CallbackQueryHandler(
        #                 callable, pattern=pattern
        #             )
        #         ],
        #         states={
        #             states.LegalSates.GET_LEGAL_LAST_NAME: [
        #                 MessageHandler(
        #                     Filters.text | Filters.command,
        #                     callbacks.get_legal_last_name,
        #                 ),
        #             ],
        #             states.LegalSates.SAVE_DATA: [
        #                 MessageHandler(
        #                     Filters.text | Filters.command, callbacks.save_legal_data
        #                 ),
        #             ],
        #         },
        #         fallbacks=[],
        #     )
        # )
