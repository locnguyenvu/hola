import abc
import inspect
from telegram import Bot

from app.bot.message import Message

class WorkFlow(metaclass=abc.ABCMeta):
    def __subclasscheck__(cls, subclass):
        return getattr(subclass, "to_dict") and callable(getattr(subclass, "to_dict"))

    @abc.abstractmethod
    def process(self, bot: Bot, message: Message):
        raise NotImplementedError

    @abc.abstractmethod
    def is_finish(self) -> bool:
        raise NotImplementedError

    def serialize(self) -> dict:
        inspect_constructor = inspect.getargspec(self.__class__.__init__)
        construct_arguments = inspect_constructor[0]

        args = []
        for argkw in construct_arguments[1:]:
            args.append(getattr(self, argkw))

        return {
            "module_path": self.__module__,
            "class_name": self.__class__.__name__,
            "arguments": args
        }
