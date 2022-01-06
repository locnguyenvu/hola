import threading
import time

from flask import current_app
from telegram import Bot
from app.auth import login_session
from app.bot.message import Message

def handle(bot: Bot, message: Message):
    user = message.get_user()
    if user is None:
        return
    ls = login_session.new_login_session(user.id)

    content = "{web_base_url}/login/{session_name}?otp={otp}".format(
            web_base_url = current_app.config["WEB_BASE_URL"],
            session_name = ls.session_name,
            otp = ls.otp)

    bot.send_message(chat_id=message.sender_id(), text=content)
    delmesg = threading.Thread(target=lambda: (
        time.sleep(10),
        bot.delete_message(chat_id=message.chat_id(), message_id=message.id)
    ), daemon=True)
    delmesg.start()