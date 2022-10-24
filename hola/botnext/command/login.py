import app.channel
from app.auth.login_session import new_login_session
from app.botnext.telegram import Message
from app.user import find_by_telegram_account
from flask import current_app
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, LoginUrl, ParseMode
from app.botnext.command.base import CommandHandler


class LoginCommand(CommandHandler):

    def require_authentication(self) -> bool:
        return True

    def _process(self, message: Message):
        user = find_by_telegram_account(str(message.from_user.username))
        ls = new_login_session(user.id)
        login_url = "{web_base_url}/login/{session_name}?otp={otp}".format(
            web_base_url=current_app.config["WEB_BASE_URL"],
            session_name=ls.session_name,
            otp=ls.otp)

        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "Login",
                    login_url=LoginUrl("{web_base_url}/telegram-login".format(web_base_url=current_app.config["WEB_BASE_URL"])),
                )
            ]
        ])
        reply_mess = message.reply_text(f"Click <a href=\"{login_url}\">here</a> to login", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        app.channel.broadcast("telegram_delete_message", dict(message_id=reply_mess.message_id, chat_id=reply_mess.chat_id, delay_time=15))
        pass
