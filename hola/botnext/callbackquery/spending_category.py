from app.botnext.workflow import WorkFlow
from app.botnext.telegram import CallbackQuery, Message
from app.botnext.chat_context import ChatContext, save as ctx_save
from app.botnext.callbackquery.base import CallbackQueryHandler
from app.i18n import t

import app.spending.category as spending_category
import app.util as util


class AddSpendingCategoryWorkFlow(WorkFlow):

    def __init__(self, name, display_name, limit):
        self.name = name
        self.display_name = display_name
        self.limit = limit
        self.done = False
        pass

    def process(self, message: Message):

        if self.name is None:
            cat = spending_category.find({"name": message.text})
            if len(cat) > 0:
                message.bot.send_message(chat_id=message.chat.id, text=t("name has already exists"))
                return

            self.name = message.text
            message.bot.send_message(chat_id=message.chat.id, text=t("telegram_bot.callbackquery.edit_spending_category_promp_2"))
            return

        if self.display_name is None:
            if message.text.isnumeric() or len(message.text) < 5:
                message.bot.send_message(chat_id=message.chat.id, text=t("invalid display name"))
                return
            self.display_name = message.text
            message.bot.send_message(chat_id=message.chat.id, text=t("telegram_bot.callbackquery.edit_spending_category_promp_3"))
            return

        if self.limit is None:
            if not util.strings.is_numeric(message.text):
                message.bot.send_message(chat_id=message.chat.id, text="invalid limit")
                return
            cat = spending_category.Category(self.name, self.display_name, float(util.strings.toint_sipostfix(message.text)))
            spending_category.save(cat)
            message.bot.send_message(chat_id=message.chat.id, text="\n".join([
                cat.display_name,
                "{}: {:,}".format(t("limitation"), cat.monthly_limit)
            ]))
            self.done = True
        pass

    def is_finish(self) -> bool:
        return self.done
    pass


class AddSpendingCategory(CallbackQueryHandler):

    def _process(self, query: CallbackQuery):
        args = query.function_arguments()
        message = query.message

        message.from_user.id = args['user_id']
        message.from_user.username = args['user_name']

        wflow = AddSpendingCategoryWorkFlow(None, None, None)
        ctx = ChatContext(__name__, wflow, message)
        ctx_save(ctx)
        message.bot.send_message(chat_id=message.chat.id, text=t("telegram_bot.callbackquery.add_spending_category_promp_1"))
        pass


class EditSpendingCategoryWorkFlow(WorkFlow):

    def __init__(self, category_id, display_name, limit):
        self.category_id = category_id
        self.display_name = display_name
        self.limit = limit
        self.done = False
        pass

    def process(self, message: Message):

        if self.category_id is None:
            if not message.text.isnumeric():
                message.bot.send_message(chat_id=message.chat.id, text="invalid id")
                return
            cat = spending_category.find_id(message.text)
            if cat is None:
                message.bot.send_message(chat_id=message.chat.id, text="invalid id")
                return
            self.category_id = message.text
            message.bot.send_message(chat_id=message.chat.id, text=t("telegram_bot.callbackquery.edit_spending_category_promp_2"))
            return

        cat = spending_category.find_id(self.category_id)
        if self.display_name is None:
            if not message.text.isnumeric():
                self.display_name = message.text
            else:
                self.display_name = cat.display_name
            message.bot.send_message(chat_id=message.chat.id, text=t("telegram_bot.callbackquery.edit_spending_category_promp_3"))
            return

        if self.limit is None:
            if not util.strings.is_numeric(message.text):
                message.bot.send_message(chat_id=message.chat.id, text="invalid limit")
                return
            cat.monthly_limit = float(util.strings.toint_sipostfix(message.text))
            spending_category.save(cat)
            message.bot.send_message(chat_id=message.chat.id, text="\n".join([
                cat.display_name,
                "{}: {:,}".format(t("limitation"), cat.monthly_limit)
            ]))
            self.done = True

        pass

    def is_finish(self) -> bool:
        return self.done
    pass


class EditSpendingCategory(CallbackQueryHandler):

    def _process(self, query: CallbackQuery):
        args = query.function_arguments()
        message = query.message

        message.from_user.id = args['user_id']
        message.from_user.username = args['user_name']

        message.bot.send_message(chat_id=message.chat.id, text=t("telegram_bot.callbackquery.edit_spending_category_promp_1"))

        wflow = EditSpendingCategoryWorkFlow(None, None, None)
        ctx = ChatContext(__name__, wflow, message)
        ctx_save(ctx)
        pass
