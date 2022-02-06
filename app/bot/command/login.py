import threading
import time

from flask import current_app
from telegram import Bot, ParseMode
from app.auth import login_session
from app.bot.message import Message

def handle(bot: Bot, message: Message):
    user = message.user
    if user is None:
        return
    ls = login_session.new_login_session(user.id)

    login_url = "{web_base_url}/login/{session_name}?otp={otp}".format(
            web_base_url = current_app.config["WEB_BASE_URL"],
            session_name = ls.session_name,
            otp = ls.otp)
    content = f"Click <a href=\"{login_url}\">here</a> to login"

    reply_mess = bot.send_message(chat_id=message.sender_id(), text=content, parse_mode=ParseMode.HTML)
    delmesg = threading.Thread(target=lambda: (
        time.sleep(2*60),
        bot.delete_message(chat_id=message.chat_id(), message_id=message.id),
        bot.delete_message(message_id=reply_mess.message_id, chat_id=reply_mess.chat_id)
    ), daemon=True)
    delmesg.start()
