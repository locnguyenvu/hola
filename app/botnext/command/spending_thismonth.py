from app.util import dt
from app.spending.log import find as spendinglog_find
from .base import CommandHandler
from telegram import Message, ParseMode


class SpendingThisMonthCommand(CommandHandler):

    def require_authentication(self) -> bool:
        return True

    def _process(self, message: Message):
        timespan = dt.time_range_from_text(dt.CURRENT_MONTH)
        logs = spendinglog_find(dict(from_date=timespan[0], to_date=timespan[1]))

        debit_amount = 0
        credit_amount = 0
        total_amount = 0
        for log in logs:
            if log.is_credit():
                credit_amount += log.amount
            if log.is_debit():
                debit_amount += log.amount

            total_amount += log.amount

        content = "\n".join([
            "```",
            f'{"D":2}| {debit_amount:>15,}',
            f'{"C":2}| {credit_amount:>15,}',
            '{:->19}'.format('-'),
            f'{"T":2}| {total_amount:>15,}',
            "```",
        ])
        message.bot.send_message(chat_id=message.chat.id, text=content, parse_mode=ParseMode.MARKDOWN_V2)
        pass
