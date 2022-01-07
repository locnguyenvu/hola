from typing import Callable

from app.di import get_bot
from app.user import find_by_telegram_account
from .message import Message
from .callback_query import CallbackQuery
from .groupchat_listener import spending_log

bot = get_bot()
class Distpatcher(object):

    commands = {}

    callback_funtions = {}

    def __init__(self):
        pass

    def register_command(self, cmd: str, handler: Callable):
        self.commands[cmd] = handler

    def register_callback(self, name: str, handler: Callable):
        self.callback_funtions[name] = handler

    def is_chat_message(self, payload: dict) -> bool:
        return "message" in payload

    def is_callback_query(self, payload: dict) -> bool:
        return "callback_query" in payload

    def dispatch(self, payload: dict):

        if self.is_chat_message(payload):
            message = Message(payload)
            self.handle_chat_message(message)
        
        if self.is_callback_query(payload):
            callback_query = CallbackQuery(payload)
            self.handle_callback_query(callback_query)

        pass

    def handle_chat_message(self, message: Message):
        user = find_by_telegram_account(str(message.sender_id()))
        if user is None:
            bot.send_message(chat_id=message.chat_id(), text="Sorry, I don't know you")
            return

        message.set_user(user)
        if message.is_command():
            for cmd in self.commands:
                if cmd == message.get_command():
                    handler = self.commands[cmd]
                    handler(bot, message)
                    break
            return
        
        if message.is_from_spending_group():
            spending_log.handle(bot, message)
            return 

    def handle_callback_query(self, callback_query: CallbackQuery):
        for func_name in self.callback_funtions.keys():
            if callback_query.func_name == func_name:
                func = self.callback_funtions[func_name]
                args = callback_query.params
                args["bot"] = bot
                args["callback_query"] = callback_query
                func(**args)
                return
        pass
