from telegram import Bot

from .base import WorkFlow
from app.bot.message import Message
from app.income.log import Log, save

class IncomeInputWorkFlow(WorkFlow):

    def __init__(self, mess = None):
        self.mess = mess
        pass

    def process(self, bot: Bot, message: Message):
        if message.is_command():
            bot.send_message(chat_id=message.chat_id(), text="Following pattern <subject> <amount>")
            return

        log = Log.from_plain_str(message.text)
        save(log)
        self.income_id = log.id
        bot.send_message(chat_id=message.chat_id(), text=f"{log.subject} => {log.amount:,}")
        pass

    def is_finish(self) -> bool:
        return hasattr(self, "income_id")