import threading
import time

from telegram import Bot
from app.bot.callback_query import CallbackQuery

def handle(bot: Bot, callback_query: CallbackQuery, category_id:str):

    bot.edit_message_text(chat_id=callback_query.chat_id(), message_id=callback_query.message_id(), text=f"Hello, world {category_id}")
    delmesg = threading.Thread(target=lambda: (
        time.sleep(10),
        bot.delete_message(chat_id=callback_query.chat_id(), message_id=callback_query.message_id())
    ), daemon=True)
    delmesg.start()
    pass