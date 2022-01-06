import re
from flask import current_app
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

import app.recommendation.spending_log_category as recommendation_spending_log_category
from app.bot.message import Message


def handle(bot: Bot, message: Message):
    msg_content = message.get_content()
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

    keyboard = [
            [
                InlineKeyboardButton(
                    f"{category.display_name}", 
                    callback_data=f"map_spending_category|category_id={category.id}")
            ]
            for category in categories
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(message.chat_id(), spending_subject, reply_markup=reply_markup)
    pass