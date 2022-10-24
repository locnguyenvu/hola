from app.i18n import t
from telegram import Message
from app.botnext.command.base import CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class SetupCommand(CommandHandler):

    def require_authentication(self) -> bool:
        return True

    def _process(self, message: Message):
        keyboard = [
            [
                InlineKeyboardButton(
                    t("telegram_bot.callbackquery.setup_spending_log_chatgroup"),
                    callback_data="setup_spending_log_chatgroup|")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message.bot.send_message(message.chat_id, text=t("setup"), reply_markup=reply_markup)
