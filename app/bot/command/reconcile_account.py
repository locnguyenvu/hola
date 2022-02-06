from telegram import Bot

import app.bot.chat_context
from app.bot.message import Message
from app.bot.workflow.reconcile_account import ReconcileAccountWorkFlow

def handle(bot: Bot, message: Message):
    app.bot.chat_context.terminate_old_context(str(message.sender_id()), str(message.chat_id()))

    workflow = ReconcileAccountWorkFlow()
    ctx = app.bot.chat_context.ChatContext()
    ctx.set_handler(workflow)
    ctx.context = __name__
    ctx.is_active = 1
    ctx.telegram_userid = str(message.sender_id())
    ctx.telegram_username = str(message.sender_username())
    ctx.chat_id = str(message.chat_id())
    ctx.handle(bot, message)
    app.bot.chat_context.save(ctx)
    pass