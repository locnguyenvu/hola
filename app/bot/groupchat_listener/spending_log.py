import threading
import time

from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from urllib.parse import urlencode

import app.recommendation.spending_log_category as recommendation_spending_log_category
import app.spending.log as spending_log
import app.spending.category as spending_category
from app.bot.message import Message


def handle(bot: Bot, message: Message):
    try:
        sl = spending_log.new_from_chat_content(message.get_content())
        sl.telegram_message_id = message.id
        sl.created_by = message.sender_username()
        spending_log.save(sl)
        categories = []
        if message.has_option("m"):
            categories = spending_category.list_all()
        else:
            categories = recommendation_spending_log_category.list_categories(sl.subject)
        keyboard = [
                [
                    InlineKeyboardButton(
                        f"{category.display_name}", 
                        callback_data="map_spending_category|{callback_params}".format(
                            callback_params = urlencode({
                                "log_id": sl.id,
                                "category_id": category.id,
                            })
                        ))
                ]
                for category in categories
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        reply_mess = bot.send_message(message.chat_id(), sl.subject, reply_markup=reply_markup)
        delmesg = threading.Thread(target=lambda: (
            time.sleep(60),
            bot.delete_message(message_id=reply_mess.message_id, chat_id=reply_mess.chat_id)
        ), daemon=True)
        delmesg.start()
    except ValueError as e:
        bot.delete_message(message_id=message.id, chat_id=message.chat_id()),
        reply_mess = bot.send_message(message.chat_id(), f"❌ {str(e)}")
        delmesg = threading.Thread(target=lambda: (
            time.sleep(5),
            bot.delete_message(message_id=reply_mess.message_id, chat_id=reply_mess.chat_id)
        ), daemon=True)
        delmesg.start()
    pass
