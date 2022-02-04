from . import auth_command
from . import recommendation_command
from . import email_command
from . import crawler_command

def init_app(app):
    app.cli.add_command(auth_command.cli)
    app.cli.add_command(recommendation_command.cli_spendinglog)
    app.cli.add_command(email_command.cli)
    app.cli.add_command(crawler_command.cli)
