import app.dbconfig
from app.i18n import t
from flask import current_app
from app.botnext.telegram import CallbackQuery
from app.botnext.callbackquery.base import CallbackQueryHandler


class SetupSpendingLogGroupChat(CallbackQueryHandler):

    def _process(self, query: CallbackQuery):
        message = query.message
        chat_id = message.chat.id
        current_app.config["telegram.group.spending_log"] = str(chat_id)
        app.dbconfig.set("telegram.group.spending_log", str(chat_id))
        message.bot.send_message(chat_id=chat_id, text=t("telegram_bot.command.init_spending_log_group.success"))
        pass
