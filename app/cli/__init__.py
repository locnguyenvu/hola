import click
from flask.cli import with_appcontext

from . import auth_command
from . import recommendation_command
from . import email_command
from app.spending.log import new_from_chat_content

@click.command("test")
@click.argument("content")
@with_appcontext
def test(content):
    from rich import inspect
    sl = new_from_chat_content(content)
    inspect(sl)



def init_app(app):
    app.cli.add_command(test)
    app.cli.add_command(auth_command.cli)
    app.cli.add_command(recommendation_command.cli_spendinglog)
    app.cli.add_command(email_command.cli)
