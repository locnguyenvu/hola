from urllib.parse import urlencode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Message
from app.i18n import t
from .base import CommandHandler

import app.spending.category as spending_category


class SpendingCategoryCommand(CommandHandler):

    def require_authentication(self) -> bool:
        return True

    def _process(self, message: Message):
        try:
            categories_message = []
            categories = spending_category.list_all()
            for cat in categories:
                monthly_limit = f"* {cat.monthly_limit:,}" if cat.monthly_limit is not None and cat.monthly_limit > 0 else ""
                categories_message.append(f"{cat.id:>3}. {cat.display_name} {monthly_limit}")
            keyboard = [
                [
                    InlineKeyboardButton(
                        t("add"),
                        callback_data="spending_category_add|{callback_params}".format(
                            callback_params=urlencode({
                                "user_id": message.from_user.id,
                                "user_name": message.from_user.username,
                            })
                        )),
                    InlineKeyboardButton(
                        t("edit"),
                        callback_data="spending_category_edit|{callback_params}".format(
                            callback_params=urlencode({
                                "user_id": message.from_user.id,
                                "user_name": message.from_user.username,
                            })
                        ))
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            message.bot.send_message(message.chat_id, text="\n".join(categories_message), reply_markup=reply_markup)
        except ValueError:
            pass
    pass
