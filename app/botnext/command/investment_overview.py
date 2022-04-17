from app.botnext.command.base import CommandHandler
from app.botnext.telegram import Message
from app.report.investment import overview as investment_overview
from telegram import ParseMode


class InvestmentOverviewCommand(CommandHandler):

    def _process(self, message: Message):
        report = investment_overview()
        content = "\n".join([
            'Interest ||*{:,}*|| \\(_{}_\\)'.format(
                round(report["net_interest"], 0),
                report["interest_rate"]).replace('.', '\\.'),
        ])
        content = content.replace('-', '\\-')
        message.bot.send_message(chat_id=message.chat.id, text=content, parse_mode=ParseMode.MARKDOWN_V2)
        pass
