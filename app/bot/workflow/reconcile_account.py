from telegram import Bot

from .base import WorkFlow
from app.bot.message import Message

class ReconcileAccountWorkFlow(WorkFlow):

    def __init__(self, cash = None, bank_balance = None, ewallet = None):
        self.cash = cash
        self.bank_balance = bank_balance
        self.ewallet = ewallet
        pass

    def process(self, bot: Bot, message: Message):
        if message.is_command():
            bot.send_message(chat_id=message.chat_id(), text="Tiền mặt:")
            return
        if not self.cash:
            self.cash = float(message.text)
            bot.send_message(chat_id=message.chat_id(), text="Số dư ngân hàng")
            return
        if not self.bank_balance:
            self.bank_balance = float(message.text)
            bot.send_message(chat_id=message.chat_id(), text="Số dư ví điện tử")
            return
        if not self.ewallet:
            self.ewallet = float(message.text)

        bot.send_message(chat_id=message.chat_id(), text="\n".join([
            f"Tiền mặt: {self.cash:,}",
            f"Số dư ngân hàng: {self.bank_balance:,}",
            f"Số dư ví điện tử: {self.ewallet:,}",
        ]))
        pass

    def is_finish(self) -> bool:
        return self.cash != None and self.bank_balance != None and self.ewallet != None