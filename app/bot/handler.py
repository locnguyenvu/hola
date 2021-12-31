from ..telebot import get_bot
from .message import Message
from abc import ABC, abstractmethod

bot = get_bot()

class Handler(ABC):

    Bot = bot

    def __init__(self):
        pass


    def reply(self, message: str):
        self.Bot.send_message(
            chat_id = self.message.sender_id(),
            text = message
        )

    @abstractmethod
    def process(self):
        pass

    def __call__(self, message: Message):
        self.message = message
        self.process()

class UnauthorizeUserHandler(Handler):
    def process(self):
        self.reply("Sorry, I don't know you! My father told me not to talk to stranger!")

class LoginHandler(Handler):
    
    def process(self):
        self.reply("HELLO, WORLD")
        pass

