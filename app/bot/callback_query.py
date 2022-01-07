from urllib.parse import parse_qs
from .message import Message

def parse_xformdata(formdata:str) -> dict:
    rawdict = parse_qs(formdata)
    result = {}
    for key in rawdict.keys():
        value = rawdict[key]
        if len(value) == 1:
            result[key] = value[0]
            continue
        result[key] = value
    return result
class CallbackQuery:
    """payload structure:
    {
        'update_id': -1,
        'callback_query': {
            'id': '-1',
            'from': {'id': -1, 'is_bot': False, 'first_name': 'Loc', 'last_name': 'Nguyen Vu', 'username': '*_*', 'language_code': 'en'},
            'message': {
                'message_id': 62,
                'from': {'id': -1, 'is_bot': True, 'first_name': '_-_', 'username': '_-_'},
                'chat': {'id': -1, 'title': '++', 'type': '++'},
                'date': 1641302737,
                'text': 'hello world',
                'reply_markup': {
                    'inline_keyboard': [
                        [{'text': 'Option 1', 'callback_data': 'Data1'}],
                        [{'text': 'Option 2', 'callback_data': 'Data2'}],
                    ]
                }
            },
            'chat_instance': '-1',
            'data': 'Data2'
        }
    }
    """
    def __init__(self, payload: dict):
        self.update_id = payload["update_id"]
        self.data = payload["callback_query"]["data"]
        self.chat_instance = payload["callback_query"]["chat_instance"]
        
        self.message = Message({
            "update_id": payload["update_id"], 
            "message": payload["callback_query"]["message"]
        })

        data_chunks = self.data.split('|')
        self.func_name = data_chunks[0]
        self.params = parse_xformdata(data_chunks[1])

    def message_id(self):
        return self.message.id

    def chat_id(self):
        return self.message.chat_id()