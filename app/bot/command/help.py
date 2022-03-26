from telegram import Bot


from app.bot.message import Message
from app.i18n import t

content = """
/init_slg {init_spending_log_group_instruct}
/tm {this_month_instruct}
"""

def handle(bot: Bot, message: Message):
    message_content = content.format(
            init_spending_log_group_instruct=t("telegram_bot.command.help.desc_init_slg"),
            this_month_instruct=t("telegram_bot.command.help.desc_tm"))
    bot.send_message(chat_id=message.chat_id(), text=message_content)
    pass
