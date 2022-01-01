from app import login_session, telebot
from flask import current_app

from .message import Message
from abc import ABC, abstractmethod

bot = telebot.get_bot()

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
        user = self.message.get_user()
        if user is None:
            return
        ls = login_session.new_login_session(user.id)

        message = "{web_base_url}/login/{session_name}?otp={otp}".format(
                web_base_url = current_app.config["WEB_BASE_URL"],
                session_name = ls.session_name,
                otp = ls.otp)

        self.reply(message)
        pass

