from abc import abstractmethod
from app.botnext.callback_query import CallbackQuery
from app.user import find_by_telegram_account


class CallbackQueryHandler(object):

    @abstractmethod
    def _process(self, query: CallbackQuery):
        raise NotImplementedError

    def execute(self, query: CallbackQuery):
        if find_by_telegram_account(query.from_user.username) is None:
            return
        self._process(query)
        pass
