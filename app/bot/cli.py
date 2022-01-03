import click
from flask.cli import with_appcontext
from app.di import get_bot

bot = get_bot()

@click.command("bot-setup")
@with_appcontext
@click.argument('base_url')
def cmd_bot_setup(base_url):
    result = bot.setWebhook('{base_url}'.format(base_url=base_url))
    print("Setup bot webhook result: {}".format(result))
