import app.dbconfig
from app.i18n import t
from flask import current_app
from telegram import Message
from app.botnext.command.base import CommandHandler


class SetupSpendingLogGroupChatCommand(CommandHandler):

    def require_authentication(self) -> bool:
        return True

    def _process(self, message: Message):
        chat_id = message.chat.id
        current_app.config["telegram.group.spending_log"] = chat_id
        app.dbconfig.set("telegram.group.spending_log", str(chat_id))
        message.bot.send_message(chat_id=chat_id, text=t("telegram_bot.command.init_spending_log_group.success"))
        pass
