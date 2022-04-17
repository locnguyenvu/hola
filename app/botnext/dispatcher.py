from app.di import get_bot
from flask import current_app
from .callbackquery.base import CallbackQueryHandler
from .chat_context import find_active as ctx_find_active, save as ctx_save
from .command.base import CommandHandler
from .groupchat.spending_log import SpendingLogGroupChat
from .telegram import Message, CallbackQuery

bot = get_bot()


class Dispatcher(object):

    commands = {}

    callback_queries = {}

    groupchats = {}

    def __init__(self):
        pass

    def register_command(self, cmd: str, handler: CommandHandler):
        self.commands[cmd] = handler
        pass

    def register_callback(self, name: str, handler: CallbackQueryHandler):
        self.callback_queries[name] = handler

    def dispatch(self, telegram_request: dict):

        if "callback_query" in telegram_request:
            callback_query = CallbackQuery.de_json(telegram_request["callback_query"], bot)
            if callback_query.function_name() in self.callback_queries:
                handler = self.callback_queries[callback_query.function_name()]
                handler.execute(callback_query)
            return

        if "message" in telegram_request:
            message = Message.de_json(telegram_request["message"], bot)
            if message.is_command():
                if message.command() not in self.commands:
                    return
                handler = self.commands[message.command()]
                handler.execute(message)
                return
            else:
                if str(message.chat.id) == current_app.config.get("telegram.group.spending_log"):
                    handler = SpendingLogGroupChat()
                    handler.execute(message)
                    return

                chat_ctx = ctx_find_active(str(message.from_user.id), str(message.chat.id))
                if chat_ctx is not None:
                    chat_ctx.handle(message)
                    ctx_save(chat_ctx)

            return

    pass
