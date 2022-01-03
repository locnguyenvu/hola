from flask import g

from app.user import find_by_telegram_account
from .message import Message
from .handler import UnauthorizeUserHandler

class Distpatcher(object):

    routes = {}

    def __init__(self):
        pass

    def register_command(self, command: str, handler):
        self.routes[command] = handler

    def dispatch(self, message: Message):

        user = find_by_telegram_account(str(message.sender_id()))
        if user is None:
            handler = UnauthorizeUserHandler()
            handler(message)
            return 

        message.set_user(user)

        if message.is_command():
            for route in self.routes:
                if route == message.get_command():
                    handler = self.routes[route]
                    handler(message)
                    break
        
        pass
