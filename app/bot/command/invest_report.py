from datetime import datetime
from telegram import Bot, ParseMode

import app.report.investment
from app.bot.message import Message
from app.util import dt

def handle(bot: Bot, message: Message):
    report = app.report.investment.overview()
    time = datetime.now()
    content = "\n".join([
        'Update on ' + time.strftime('%Y\-%m\-%d'),
        'Interest \(_{}_\) *{:,}*'.format(report["interest_rate"], round(report["net_interest"], 0)).replace('.', '\.'),
    ])
    bot.send_message(chat_id=message.chat_id(), text=content, parse_mode=ParseMode.MARKDOWN_V2)
