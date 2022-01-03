import click
from flask import current_app
from flask.cli import with_appcontext

from . import auth_command
from . import recommendation_command

@click.command("config-set")
@with_appcontext
@click.argument("key")
@click.argument("value")
def test(key, value):
    current_app.config[key] = value
    print(current_app.config.get(key))

@click.command("test")
@with_appcontext
def test():
    from rich import print
    print(current_app.config.get("telegram.group.spending_log"))
    for key in current_app.config.keys():
        print(key)



def init_app(app):
    app.cli.add_command(test)
    app.cli.add_command(auth_command.cli)
    app.cli.add_command(recommendation_command.cli_spendinglog)