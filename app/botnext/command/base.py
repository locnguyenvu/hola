from abc import abstractmethod
from app.user import find_by_telegram_account
from app.i18n import t
from telegram import Message


class CommandHandler(object):

    @abstractmethod
    def _process(self, message: Message):
        raise NotImplementedError

    def require_authentication(self) -> bool:
        return True

    def execute(self, message: Message):
        if self.require_authentication() and find_by_telegram_account(str(message.from_user.username)) is None:
            message.reply_text(t("telegram_bot.authentication_failed"))
            return
        self._process(message)
        pass

    pass
