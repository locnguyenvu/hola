import click
from flask import current_app 
from flask.cli import with_appcontext
from telegram import Bot

@click.command("bot-setup")
@with_appcontext
@click.argument('base_url')
def cmd_bot_setup(base_url):
    bot = Bot(current_app.config["TELEGRAM_SECRET"])
    result = bot.setWebhook('{base_url}/telegram'.format(base_url=base_url))
    print("Setup bot webhook result: {}".format(result))
