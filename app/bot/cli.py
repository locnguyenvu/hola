from flask import current_app
import click
from flask.cli import with_appcontext
from app.di import get_bot

bot = get_bot()

@click.command("bot-setup")
@with_appcontext
@click.argument('base_url')
def cmd_bot_setup(base_url):
    webhook_endpoint = f"{base_url}?x-bot={current_app.config.get('TELEGRAM_WEBHOOK_SECRET')}"
    result = bot.setWebhook(webhook_endpoint)
    print("Setup bot webhook endpoint {} result: {}".format(webhook_endpoint, result))
