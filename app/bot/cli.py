import click
from flask import current_app 
from flask.cli import with_appcontext
from telegram import Bot

@click.command("bot-setup")
@with_appcontext
def cmd_bot_setup():
    bot = Bot(current_app.config["TELEGRAM_SECRET"])
    result = bot.setWebhook('{base_url}/telegram'.format(base_url="https://bf72-27-77-244-233.ngrok.io"))
    print("Setup bot webhook result: {}".format(result))
