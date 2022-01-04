from flask import g

from app.user import find_by_telegram_account
from .message import Message
from .handler import UnauthorizeUserHandler, SpendingLogHandler

class Distpatcher(object):

    commands = {}

    def __init__(self):
        pass

    def register_command(self, cmd: str, handler):
        self.commands[cmd] = handler

    def is_chat_message(self, payload: dict) -> bool:
        return "message" in payload

    def is_callback_query(self, payload: dict) -> bool:
        return "callback_query" in payload

    def dispatch(self, payload: dict):

        if self.is_chat_message(payload):
            message = Message(payload)
            self.handle_chat_message(message)
            
        pass

    def handle_chat_message(self, message: Message):
        user = find_by_telegram_account(str(message.sender_id()))
        if user is None:
            handler = UnauthorizeUserHandler()
            handler(message)
            return 

        message.set_user(user)

        if message.is_command():
            for cmd in self.commands:
                if cmd == message.get_command():
                    handler = self.commands[cmd]
                    handler(message)
                    break
            return
        
        if message.is_from_spending_group():
            handler = SpendingLogHandler()
            handler(message)
            return 
