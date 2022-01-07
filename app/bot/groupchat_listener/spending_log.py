from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from urllib.parse import urlencode

import app.recommendation.spending_log_category as recommendation_spending_log_category
import app.spending.log as spending_log
from app.bot.message import Message


def handle(bot: Bot, message: Message):
    sl = spending_log.new_from_chat_content(message.get_content())
    sl.telegram_message_id = message.id
    sl.created_by = message.sender_username()
    sl.save()
    categories = recommendation_spending_log_category.list_category_id(sl.subject)
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
    bot.send_message(message.chat_id(), sl.subject, reply_markup=reply_markup)
    pass
