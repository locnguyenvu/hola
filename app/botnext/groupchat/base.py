from abc import abstractmethod
from app.user import find_by_telegram_account
from telegram import Message


class GroupChat(object):

    def execute(self, message: Message):
        if find_by_telegram_account(message.from_user.username) is None:
            return
        self._process(message)
        pass

    @abstractmethod
    def _process(self, message: Message):
        pass
