from app.i18n import t
from telegram import Message
from .base import CommandHandler

content = """
/tm {spending_thismonth_instruct}
"""


class HelpCommand(CommandHandler):

    def require_authentication(self) -> bool:
        return False

    def _process(self, message: Message):
        message.bot.send_message(chat_id=message.chat.id, text=content.format(
            spending_thismonth_instruct=t("telegram_bot.command.help.desc_tm"))
        )
        pass
