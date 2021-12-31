import re

class Message:

    def __init__(self, message: dict):
        self.id = message["message_id"]
        self.sender = message["from"]
        self.chat = message["chat"]
        self.text = message["text"]

    def sender_id(self) -> int:
        return self.sender["id"]

    def is_command(self) -> bool:
        return re.match(r"^\/[a-zA-Z0-9]+", self.text) != None

    def get_command(self) -> str:
        chunks = self.text.split(" ")
        return chunks[0].lstrip("/")
