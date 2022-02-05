from telegram import Bot, ParseMode

import app.spending.log as spending_log
from app.bot.message import Message
from app.util import dt

def handle(bot: Bot, message: Message):
    timespan = dt.time_range_from_text(dt.CURRENT_MONTH)
    
    slogs = spending_log.find({
        "from_date": timespan[0],
        "to_date": timespan[1]
    })

    debit_amount = 0
    credit_amount = 0
    total_amount = 0
    for slog in slogs:
        if slog.is_credit():
            credit_amount += slog.amount
        if slog.is_debit():
            debit_amount += slog.amount

        total_amount += slog.amount

    content = "\n".join([
        "```",
        f'{"D":2}| {debit_amount:>15,}',
        f'{"C":2}| {credit_amount:>15,}',
        '{:->19}'.format('-'),
        f'{"T":2}| {total_amount:>15,}',
        "```",
    ])
    bot.send_message(chat_id=message.chat_id(), text=content, parse_mode=ParseMode.MARKDOWN_V2)
