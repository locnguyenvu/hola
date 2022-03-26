from telegram import Bot
from flask import current_app

import app.dbconfig
import app.report.investment
import app.channel
from app.bot.message import Message
from app.i18n import t

def handle(bot: Bot, message: Message):
    current_app.config["telegram.group.spending_log"] = message.chat_id()
    app.dbconfig.set("telegram.group.spending_log", message.chat_id())
    _ = bot.send_message(chat_id=message.chat_id(), text=t("telegram_bot.command.init_spending_log_group.success"))
    pass
