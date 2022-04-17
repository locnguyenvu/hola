import re
from telegram import Message as BaseMessage
from telegram import CallbackQuery as BaseCallbackQuery
from urllib.parse import parse_qs


class Message(BaseMessage):

    def command(self) -> str:
        chunks = self.text.split(" ")
        return chunks[0].lstrip("/")

    def is_command(self) -> bool:
        return re.match(r"^\/[a-zA-Z0-9]+", self.text) is not None


class CallbackQuery(BaseCallbackQuery):

    def function_name(self) -> str:
        data_chunks = self.data.split('|')
        return data_chunks[0]

    def function_arguments(self) -> dict:
        data_chunks = self.data.split('|')
        rawdict = parse_qs(data_chunks[1])
        result = {}
        for key in rawdict.keys():
            value = rawdict[key]
            if len(value) == 1:
                result[key] = value[0]
                continue
            result[key] = value
        return result

    pass
