import re
import telegram
import hola.config as hola_config

from abc import abstractmethod
from flask import current_app
from hola.auth.user import find_by_telegram_info
from urllib.parse import parse_qs


class Message(telegram.Message):

    def command(self) -> str:
        chunks = self.text.split(" ")
        return chunks[0].lstrip("/")

    def is_command(self) -> bool:
        return re.match(r"^\/[a-zA-Z0-9]+", self.text) is not None


class CallbackQuery(telegram.CallbackQuery):

    def function_name(self) -> str:
        data_chunks = self.data.split('|')
        return data_chunks[0]

    def function_arguments(self) -> dict:
        data_chunks = self.data.split('|')
        rawdict = parse_qs(data_chunks[1])
        result = {}
        for key in rawdict.keys():
            value = rawdict[key]
            if len(value) == 1:
                result[key] = value[0]
                continue
            result[key] = value
        return result


class Handler:
    @abstractmethod
    def exec(self, event: telegram.TelegramObject):
        pass


class SetupCommand(Handler):
    def exec(self, event: Message):
        if event.chat.type not in [telegram.constants.ChatType.GROUP, telegram.constants.ChatType.SUPERGROUP]:
            pass
        hola_config.set('bot.group_id', str(event.chat.id))


class Dispatcher:

    def __init__(self, bot: telegram.Bot):
        self.bot = bot
        self.commands = {
            'setup': SetupCommand()
        }
        self.callback_queries = {}

    def callbackquery_handler(self, func_name: str):
        if func_name not in self.callback_queries:
            return None
        return self.callback_queries[func_name]

    def command_handler(self, command: str):
        if command not in self.commands:
            return None
        return self.commands(command)

    def process(self, payload: dict):

        if 'callback_query' in payload:
            event = CallbackQuery.de_json(payload['callback_query'], self.bot)
            if event is None:
                return
            handler = self.callbackquery_handler(event.function_name())

        if 'message' in payload:
            event = Message.de_json(payload['message'], self.bot)
            if event is None:
                return
            if event.is_command():
                handler = self.command_handler(event.command())

        user = find_by_telegram_info(event.from_user.id)
        if user is None:
            return

        if handler is None:
            return
        handler.exec(event)
        pass
