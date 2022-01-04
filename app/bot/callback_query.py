from .message import Message

class CallbackQuery:
    """
    payload structure:

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
        self.data = payload["data"]
        
        self.message = Message({
            "update_id": payload["update_id"], 
            "message": payload["callback_query"]["message"]
        })
