from flask import Flask
from click import Argument, Command
from flask.cli import with_appcontext


def init_app(app: Flask):
    import hola.auth as auth
    app.cli.add_command(Command('auth:add_user',
                                callback=with_appcontext(auth.add_user),
                                params=[
                                    Argument(['telegram_username'], required=True),
                                    Argument(['telegram_userid'], required=True),
                                ]))

    import hola.bot as bot
    app.cli.add_command(Command('bot:setup-webhook',
                                callback=with_appcontext(bot.setup_webhook_endpoint),
                                params=[
                                    Argument(['url'], required=True),
                                ]))
