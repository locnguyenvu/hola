from telegram import CallbackQuery as TgCallbackQuery
from urllib.parse import parse_qs


def parse_xformdata(formdata: str) -> dict:
    rawdict = parse_qs(formdata)
    result = {}
    for key in rawdict.keys():
        value = rawdict[key]
        if len(value) == 1:
            result[key] = value[0]
            continue
        result[key] = value
    return result


class CallbackQuery(TgCallbackQuery):

    def function_name(self) -> str:
        data_chunks = self.data.split('|')
        return data_chunks[0]

    def function_arguments(self) -> dict:
        data_chunks = self.data.split('|')
        return parse_xformdata(data_chunks[1])

    pass
