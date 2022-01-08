import threading
import time

from telegram import Bot
from app.bot.callback_query import CallbackQuery
import app.spending.log as spending_log
import app.spending.category as spending_category
import app.recommendation.spending_log_category as recommendation_spending_log_category

def handle(bot: Bot, callback_query: CallbackQuery, log_id:str, category_id:str):

    sl = spending_log.find_id(log_id)
    sc = spending_category.find_id(category_id)

    sl.spending_category_id = sc.id
    spending_log.save(sl) 

    recommendation_spending_log_category.tokenize(sl)
    bot.edit_message_text(chat_id=callback_query.chat_id(), message_id=callback_query.message_id(), text=f"{sl.subject} -> {sc.display_name}")
    delmesg = threading.Thread(target=lambda: (
        time.sleep(5),
        bot.delete_message(chat_id=callback_query.chat_id(), message_id=callback_query.message_id())
    ), daemon=True)
    delmesg.start()
    pass
