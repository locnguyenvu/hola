import re
from flask import current_app

from app.user import User

class Message(object):
    """payload structure:
    {
        'update_id': -1,
        'message': {
            'message_id': -1,
            'from': {
                'id': -1, 
                'is_bot': False, 
                'first_name': 'Loc', 
                'last_name': 'Nguyen Vu',
                'username': '*_*',
                'language_code': 'en'
            },
            'chat': {
                'id': -1, 
                'title': '++',
                'type': '++'
            },
            'reply_to_message': {
                'message_id': 100,
                'from': {
                    'id': -2,
                    'is_bot': False,
                    'first_name': 'Loc',
                    'last_name': 'Nguyen Vu',
                    'username': '*_*',
                    'language_code': 'en'
                },
                'chat': {
                    'id': -2, 
                    'title': '+++',
                    'type': '+++'
                },
                'date': 1641531176,
                'text': 'cà phê 19k'
            },
            'date': 1641302736,
            'text': 'hello world'
        }
    }
    """
    def __init__(self, payload: dict):
        self.update_id = payload["update_id"]

        message = payload["message"]
        self.id = message["message_id"]
        self.sender = message["from"]
        self.chat = message["chat"]
        self.text = message["text"]

        if "reply_to_message" in message:
            self.reply_to_message = Message({"update_id": self.update_id, "message": message["reply_to_message"]})
        else:
            self.reply_to_message = None

        self.user = None

    def sender_id(self) -> int:
        return self.sender["id"]

    def sender_username(self) -> str:
        return self.sender["username"]

    def is_command(self) -> bool:
        return re.match(r"^\/[a-zA-Z0-9]+", self.text) != None

    def get_command(self) -> str:
        chunks = self.text.split(" ")
        return chunks[0].lstrip("/")

    def get_content(self) -> str:
        clean_msg = self.text.strip(" ")
        return clean_msg

    def set_user(self, user: User):
        self.user = user

    def chat_id(self):
        return self.chat["id"]

    def is_from_spending_group(self) -> bool:
        if self.chat_id() == self.sender_id():
            return False
        return str(self.chat_id()) == current_app.config.get("telegram.group.spending_log")

    def is_a_reply(self) -> bool:
        return self.reply_to_message is not None

    def reply_message(self) -> object:
        return self.reply_to_message
