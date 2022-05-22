from flask.cli import AppGroup
from click import argument

import app.channel
from app.i18n import t

cli = AppGroup("dry-run")


@cli.command("broadcast-postgres-channel")
def broadcast_postgres_channel():
    app.channel.broadcast("news", dict(message="Hello, world"))


@cli.command("listen-postgres-channel")
def listen_postgres_channel():
    def handler(payload: dict):
        print(payload)

    app.channel.consume("news", handler)


@cli.command("i18n")
def i18n():
    print(t("telegram_bot.spending_log_wrong_group_error"))
