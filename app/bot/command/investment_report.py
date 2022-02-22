from datetime import datetime
from telegram import Bot, ParseMode

import app.report.investment
from app.bot.message import Message
from app.util import dt

def handle(bot: Bot, message: Message):
    report = app.report.investment.overview()
    content = "\n".join([
        'Interest *{:,}* \(_{}_\)'.format(round(report["net_interest"], 0),report["interest_rate"]).replace('.', '\.'),
    ])
    bot.send_message(chat_id=message.chat_id(), text=content, parse_mode=ParseMode.MARKDOWN_V2)
