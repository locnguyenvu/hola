import time
from flask.cli import AppGroup

import app.channel
from app.di import get_bot

bot = get_bot()
cli = AppGroup("background-task")
@cli.command("telegram-clean-up-message")
def clean_up_message():
    def handler(payload: dict):
        """
        Payload constract:
        {
            "message_id": <int>,
            "chat_id": <int>,
            "delay_time": <int>
        }
        """
        if "delay_time" not in payload or payload["delay_time"] > 0:
            time.sleep(payload["delay_time"]),
        bot.delete_message(message_id=payload["message_id"], chat_id=payload["chat_id"])
        pass

    app.channel.consume("telegram_delete_message", handler)
    pass

