from . import auth
from . import recommendation
from . import email
from . import crawler
from . import dryrun

def init_app(app):
    app.cli.add_command(auth.cli)
    app.cli.add_command(recommendation.cli_spendinglog)
    app.cli.add_command(email.cli)
    app.cli.add_command(crawler.cli)
    app.cli.add_command(dryrun.cli)
