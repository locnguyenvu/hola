import re
from abc import ABC, abstractmethod
from flask import current_app
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import app.recommendation.spending_log_category as recommendation_spending_log_category
from app.di import get_bot
from app.auth import login_session
from .message import Message

class Handler(ABC):

    Bot = get_bot()

    def __init__(self):
        pass


    def reply(self, message: str, **kwarg):
        kwarg["chat_id"] = self.message.chat_id()
        kwarg["text"] = message
        self.Bot.send_message(kwarg)

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

class SpendingLogHandler(Handler):

    def process(self):
        msg_content = self.message.get_content()
        msg_chunks = msg_content.split(" ")
        amount = None
        for word in msg_chunks:
            amount_match = re.search(r"^\d+kc*", word)
            if amount_match is None:
                continue
            else:
                amount = amount_match[0]

        if amount in msg_chunks:
            msg_chunks.remove(amount)
        
        spending_subject = " ".join(msg_chunks)
        categories = recommendation_spending_log_category.list_category_id(spending_subject)

        category_button = list(map(lambda cat: InlineKeyboardButton(
            cat.display_name,
            callback_data=f"MapSlCategoryCallbackQuery|categoryid={cat.id}"
        ), categories))

        keyboard = [
                [
                    InlineKeyboardButton(
                        f"{category.display_name}", 
                        callback_data=f"MapSlCategoryCallbackQuery|categoryid={category.id}")
                ]
                for category in categories
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        self.Bot.send_message(self.message.chat_id(), spending_subject, reply_markup=reply_markup)
        pass