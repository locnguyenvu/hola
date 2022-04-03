from app.di import get_bot
from flask import current_app

bot = get_bot()


def setup_webhook(endpoint_url):
    webhook_endpoint = f"{endpoint_url}?x-bot={current_app.config.get('TELEGRAM_WEBHOOK_SECRET')}"
    result = bot.setWebhook(webhook_endpoint)
    print("Setup bot webhook endpoint {} result: {}".format(webhook_endpoint, result))
