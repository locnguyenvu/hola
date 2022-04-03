from app.botnext.command.base import CommandHandler
from app.botnext.workflow import WorkFlow
from app.botnext.chat_context import ChatContext, save as ctx_save
from app.botnext.telegram import Message
from app.i18n import t
from app.income.log import Log, save


class IncomeInputWorkFlow(WorkFlow):

    def __init__(self):
        pass

    def process(self, message: Message):
        if message.is_command():
            message.bot.send_message(chat_id=message.chat.id, text=t("telegram_bot.workflow.income_input.prompt_1"))
            return

        log = Log.from_plain_str(message.text)
        save(log)
        self.income_id = log.id
        message.bot.send_message(chat_id=message.chat.id, text=f"{log.subject} => {log.amount:,}")
        pass

    def is_finish(self) -> bool:
        return hasattr(self, "income_id")
    pass


class IncomeInputCommand(CommandHandler):

    def _process(self, message: Message):
        wflow = IncomeInputWorkFlow()
        ctx = ChatContext(__name__, wflow, message)
        ctx.handle(message)
        ctx_save(ctx)
        pass
