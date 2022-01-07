import threading
import time

from flask import current_app
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, LoginUrl

from app.bot.message import Message

def handle(bot: Bot, message: Message):
    user = message.user
    if user is None:
        return

    content = f"Welcome {user.telegram_username}"
    login_url = LoginUrl(current_app.config.get("TELEGRAM_AUTH_CALLBACK"))
    keyboard = [
        [
            InlineKeyboardButton(f"Login", login_url=login_url)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)


    bot.send_message(chat_id=message.sender_id(), text=content, reply_markup=reply_markup)
    delmesg = threading.Thread(target=lambda: (
        time.sleep(10),
        bot.delete_message(chat_id=message.chat_id(), message_id=message.id)
    ), daemon=True)
    delmesg.start()
