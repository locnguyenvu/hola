from click import Argument, Command
from flask.cli import with_appcontext
from . import auth
from . import background_task
from . import recommendation
from . import email
from . import crawler
from . import dryrun
from . import bot


def init_app(app):
    app.cli.add_command(auth.cli)
    app.cli.add_command(recommendation.cli_spendinglog)
    app.cli.add_command(email.cli)
    app.cli.add_command(crawler.cli)
    app.cli.add_command(dryrun.cli)
    app.cli.add_command(background_task.cli)

    app.cli.add_command(Command('botnext-setup',
                                callback=with_appcontext(bot.setup_webhook),
                                params=[
                                    Argument(["endpoint-url"], required=True)
                                ]))
